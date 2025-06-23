from sqlalchemy.orm import Session
from sqlalchemy import and_
from sqlalchemy.orm import aliased
from itertools import product
from mail.send import send_templated_email
from models.models import Accounts  

from models.models import (
    Items,
    PersonalItems,
    Jewelry,
    Accessories,
    TravelItems,
    ElectronicDevices,
    Clothing,
    OfficeItems,
    OtherItems,
    Matches,
    CategoryEnum,
    StatusEnum,
    MatchStatusEnum,
)


def get_subclass_model(category: CategoryEnum):
    return {
        CategoryEnum.PERSONAL_ITEMS: PersonalItems,
        CategoryEnum.JEWELRY: Jewelry,
        CategoryEnum.ACCESSORIES: Accessories,
        CategoryEnum.TRAVEL_ITEMS: TravelItems,
        CategoryEnum.ELECTRONIC_DEVICES: ElectronicDevices,
        CategoryEnum.CLOTHING: Clothing,
        CategoryEnum.OFFICE_ITEMS: OfficeItems,
        CategoryEnum.OTHER_ITEMS: OtherItems,
    }[category]


def get_matching_fields_and_threshold(category: CategoryEnum):
    return {
        CategoryEnum.PERSONAL_ITEMS: (["type", "color"], 1),
        CategoryEnum.JEWELRY: (["type", "color", "size"], 2),
        CategoryEnum.ACCESSORIES: (["type", "color", "material", "brand"], 2),
        CategoryEnum.TRAVEL_ITEMS: (["type", "color", "size", "material", "brand"], 3),
        CategoryEnum.ELECTRONIC_DEVICES: (["type", "color", "material", "brand"], 3),
        CategoryEnum.CLOTHING: (["type", "color", "size", "material", "brand"], 3),
        CategoryEnum.OFFICE_ITEMS: (["type", "color", "size", "material", "name"], 3),
        CategoryEnum.OTHER_ITEMS: (["type", "color", "size", "material", "brand", "name"], 3),
    }[category]

def match_all_lost_and_found(session: Session):
    for category in CategoryEnum:
        SubModel = get_subclass_model(category)
        match_fields, threshold = get_matching_fields_and_threshold(category)

        LostAlias = aliased(SubModel)
        FoundAlias = aliased(SubModel)

        lost_items = (
            session.query(Items, LostAlias)
            .join(LostAlias, Items.id == LostAlias.item_id)
            .filter(
                Items.category == category,
                Items.status == StatusEnum.LOST
            )
            .all()
        )

        found_items = (
            session.query(Items, FoundAlias)
            .join(FoundAlias, Items.id == FoundAlias.item_id)
            .filter(
                Items.category == category,
                Items.status == StatusEnum.FOUND
            )
            .all()
        )

        for (lost_item, lost_sub), (found_item, found_sub) in product(lost_items, found_items):
            match_count = sum(
                getattr(lost_sub, attr) == getattr(found_sub, attr)
                for attr in match_fields
            )

            if match_count >= threshold:
                percentage = int((match_count / len(match_fields)) * 100)

                already_exists = session.query(Matches).filter_by(
                    lost_item_id=lost_item.id,
                    found_item_id=found_item.id
                ).first()

                if not already_exists:
                    session.add(
                        Matches(
                            lost_item_id=lost_item.id,
                            found_item_id=found_item.id,
                            status=MatchStatusEnum.UNCONFIRMED,
                            percentage=percentage
                        )
                    )

                    # Get worker (who submitted the FOUND item)
                    worker = session.query(Accounts).filter_by(email=found_item.email).first()

                    if worker:
                        send_templated_email(
                            to=worker.email,
                            template_id=10,
                            name=worker.name,
                            surname=worker.surname,
                            item_id=found_item.id,
                            item_type=found_item.category.value  # if enum, get string
                        )

    session.commit()
