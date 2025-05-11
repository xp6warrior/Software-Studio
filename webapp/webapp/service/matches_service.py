from webapp.repository.matches_repo import *
from webapp.repository.item_repo import *
from webapp.repository.account_repo import select_account
from webapp.items import *
from webapp.models.models import *

models_list = {
    cls.__tablename__: cls for name, cls in inspect.getmembers(models, inspect.isclass)
    if cls != Accounts and cls != Match
}

def get_matches(email: str) -> list:
    return_list = []
    found_models = select_items(email)

    for f_model in found_models:
        matches = select_matches(f_model.id, type(f_model))

        f_item = Found_Item(
            category=f_model.__tablename__, item_type=f_model.type, desc=f_model.description,
            item_id=str(f_model.id), color=getattr(f_model, "color", None),
            size=getattr(f_model, "size", None), material=getattr(f_model, "material", None),
            brand=getattr(f_model, "brand", None), name=getattr(f_model, "name", None)
        )
        for match in matches:
            # TODO Make it so I can use enum here
            if match.status != "unconfirmed":
                continue
            l_model = select_item_by_id(match.lost_item_id, models_list[match.table_name])

            l_item = Lost_Item(
                category=l_model.__tablename__, item_type=l_model.type, desc=l_model.description,
                item_id=str(l_model.id), color=getattr(l_model, "color", None),
                size=getattr(l_model, "size", None), material=getattr(l_model, "material", None),
                brand=getattr(l_model, "brand", None), name=getattr(l_model, "name", None),
                status=l_model.status
            )
            return_list.append([l_item, f_item, "Schema doesn't store percentage yet :P"])

    return return_list


def confirm_match(lost_item_id: int, found_item_id: int, model_cls: object):
    matches = select_matches(found_item_id, model_cls)
    for m in matches:
        if m.lost_item_id == lost_item_id:
            m.status = MatchStatus.CONFIRMED
            insert_update_match(m)
            break

def get_confirmed_matches_with_user_pesel(email: str):
    return_list = []
    models = select_items(email)
    # Assumes all selected items are found, since the email belongs to the worker
    for model in models:
        matches = select_matches(model.id, type(model))

        for match in matches:
            # TODO Make it so I can use enum here
            if match.status == "confirmed":
                l_model = select_item_by_id(match.lost_item_id, type(model))
                owner = select_account(l_model.email)

                m_item = Matched_Item(
                    category=l_model.__tablename__, item_type=l_model.type, desc=l_model.description,
                    item_id=str(l_model.id), color=getattr(l_model, "color", None),
                    size=getattr(l_model, "size", None), material=getattr(l_model, "material", None),
                    brand=getattr(l_model, "brand", None), name=getattr(l_model, "name", None),
                    pesel=str(owner.pesel)
                )
                return_list.append(m_item)

    return return_list