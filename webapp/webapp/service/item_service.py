import inspect
import re
import webapp.models.models as models
from webapp.models.archive_models import *
from webapp.models.enums import MatchStatus
from webapp.repository.item_repo import *
from webapp.repository.matches_repo import select_matches
from webapp.repository.account_repo import select_account_by_email
from webapp.items import *

models_list = [cls for name, cls in inspect.getmembers(models, inspect.isclass)
               if cls != models.Accounts and cls != models.Match]
archive_models = {
    models.PersonalItems: ArchivePersonalItems,
    models.Jewelry: ArchiveJewelry,
    models.Accessories: ArchiveAccessories,
    models.TravelItems: ArchiveTravelItems,
    models.ElectronicDevices: ArchiveElectronicDevices,
    models.Clothing: ArchiveClothing,
    models.OfficeItems: ArchiveOfficeItems,
    models.OtherItems: ArchiveOtherItems
}
# TODO Better email verification
email_regex = r"^[^@]+@[^@]+\.[^@]+$"

def get_submitted_lost_items(email: str) -> list[Lost_Item]:
    if re.match(email_regex, email) == None:
        raise Exception(f"Invalid email address! {email}")

    models = select_items(email)
    return_list = []

    for model in models:
        item = Lost_Item(
            category=model.__tablename__,
            item_type=model.type,
            desc=model.description,
            status=model.status,
            item_id=str(model.id),
            color=getattr(model, "color", None),
            size=getattr(model, "size", None),
            material=getattr(model, "material", None),
            brand=getattr(model, "brand", None),
            name=getattr(model, "name", None)
        )

        matches = select_matches(model.id, type(model))
        for match in matches:
            # TODO Make it so I can use enum here
            if match.status == "confirmed":
                item.status = "confirmed"
                break

        return_list.append(item)

    return return_list

def submit_lost_item(email: str, item: Lost_Item):
    model = create_model_from_item(item.category, item, email)
    if model == None:
        raise Exception(f"Invalid item cateogory! {item.category}")
    
    # TODO Make it so I can use the enum here
    model.status = "lost"
    insert_update_item(model)

def submit_found_item(email: str, item: Found_Item):
    model = create_model_from_item(item.category, item, email)
    if model == None:
        raise Exception(f"Invalid item cateogory! {item.category}")
    
    # TODO Make it so I can use the enum here
    model.status = "found"
    insert_update_item(model)

# TODO change model_name:str back to model_cls:object
def delete_lost_item(email: str, id: int, model_name: str):
    model_cls = None
    for m in models_list:
        if m.__tablename__ == model_name:
            model_cls = m
    if model_cls == None:
        return None
    
    selected = select_item_by_id(id, model_cls)
    if selected == None:
        raise Exception(f"{model_cls.__name__} of id {id} does not exist!")
    if selected.email != email:
        raise Exception("Attempt to delete item of other user!")
    delete_item(selected)

def hand_over_and_archive_match(id: int, model_name: str):
    model_cls = None
    for m in models_list:
        if m.__tablename__ == model_name:
            model_cls = m
    if model_cls == None:
        return None
    
    f_model = select_item_by_id(id, model_cls)
    matches = select_matches(id, model_cls)

    for m in matches:
        if m.status == MatchStatus.CONFIRMED:
            l_model = select_item_by_id(m.lost_item_id, model_cls)
            owner = select_account(l_model.email)

            data = f_model.dict()
            data.pop("status")
            data["email"] = owner.email
            data["username"] = owner.name
            data["surname"] = owner.surname
            data["pesel"] = owner.pesel

            archive_cls = archive_models[model_cls]
            archive_model = archive_cls(**data)

            insert_update_item(archive_model)
            delete_item(f_model)
            delete_item(l_model)
            delete_item(m)
            break


def create_model_from_item(model_name: str, item: Item, email: str) -> object:
    model_cls = None
    for m in models_list:
        if m.__tablename__ == model_name:
            model_cls = m
    if model_cls == None:
        return None
    
    model = model_cls(
        type=item.item_type,
        email=email,
        description=item.desc
    )
    if item.color != None and hasattr(model, "color"):
        model.color = item.color
    if item.size != None and hasattr(model, "size"):
        model.size = item.size
    if item.material != None and hasattr(model, "material"):
        model.material = item.material
    if item.brand != None and hasattr(model, "brand"):
        model.brand = item.brand
    if item.name != None and hasattr(model, "name"):
        model.name = item.name

    return model