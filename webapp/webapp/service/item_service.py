from webapp.models2.models import Items
from webapp.models2.enums import MatchStatusEnum, RoleEnum
from webapp.repository.item_repo import *
from webapp.repository.account_repo import select_account_by_email
from webapp.repository.matches_repo import select_matches_by_item, select_false_pickup_matches
from webapp.repository.image_repo import *
from sqlalchemy.orm.attributes import InstrumentedAttribute
from sqlalchemy.dialects.postgresql import ENUM as PG_ENUM
from sqlalchemy.sql.sqltypes import Enum as SA_ENUM

category_to_class_map = {
    cls.__mapper_args__["polymorphic_identity"].value: cls
    for cls in Items.__subclasses__()
}

def get_submitted_lost_items(user_email: str) -> list[dict[str, str]]:
    items_list = []
    items = select_items_by_email(user_email)
    if items == []:
        return False
    
    for i in items:
        status = ""

        matches = select_matches_by_item(i)
        if matches == []:
            status = "Pending"
        else:
            for m in matches:
                if m.status == MatchStatusEnum.CONFIRMED:
                    status = "Matched"
                    break
                elif m.status == MatchStatusEnum.PICKED_UP:
                    status = "Picked up"
                    break
                elif m.status == MatchStatusEnum.FALSE_PICKUP:
                    status = "Under review"
                    break
                else:
                    status = "Under review"
        item_dict = i.to_dict()
        item_dict["status"] = status
        items_list.append(item_dict)
    
    return items_list

def submit_item(email: str, item: dict[str, str]):
    cls = category_to_class_map.get(item["category"])
    i = cls()

    item['type'] = item.pop('it')
    item['description'] = item.pop('desc')

    for k, v in item.items():
        if k != "category" and hasattr(i, k):
            attr = getattr(type(i), k, None)

            if isinstance(attr, InstrumentedAttribute):
                col_type = attr.property.columns[0].type

                if isinstance(col_type, (SA_ENUM, PG_ENUM)):
                    enum_class = col_type.enum_class
                    v = enum_class(v)

            setattr(i, k, v)

    acc = select_account_by_email(email)
    i.email = email
    if acc.role == RoleEnum.USER:
        i.status = StatusEnum.LOST
    elif acc.role == RoleEnum.WORKER:
        i.status = StatusEnum.FOUND

    try:
        insert_update_item(i)
    except:
        return "Error when submitting item"
    if 'image' in item and item['image'] is not None:
        save_image(str(i.id), item['image'])
    return "Item successfully submitted"

def update_lost_item(user_email: str, item_id: str, item: dict[str, str]):
    i = select_item_by_id(int(item_id))
    if i.email == user_email:
        item['description'] = item.pop('desc')

        for k, v in item.items():
            if k != "category" and hasattr(i, k):
                attr = getattr(type(i), k, None)

                if isinstance(attr, InstrumentedAttribute):
                    col_type = attr.property.columns[0].type

                    if isinstance(col_type, (SA_ENUM, PG_ENUM)):
                        enum_class = col_type.enum_class
                        v = enum_class(v)

                setattr(i, k, v)

        try:
            insert_update_item(i)
        except:
            return "Error when submitting item"
        if 'image' in item and item['image'] is not None:
            update_image(str(i.id), item['image'])
        return "Item successfully submitted"
        
    else:
        return "Error when submitting item"

def delete_lost_item(user_email: str, item_id: str) -> bool:
    item = select_item_by_id(int(item_id))
    if item is not None and item.email == user_email:
        delete_image(item_id)
        delete_item(int(item_id))
        return True
    else:
        return False

def report_false_pickup(user_email: str, item_id: str):
    item = select_item_by_id(int(item_id))
    if item is not None and item.email == user_email:
        matches = select_matches_by_item(item)
        for m in matches:
            if m.status == MatchStatusEnum.PICKED_UP:
                m.status = MatchStatusEnum.FALSE_PICKUP
                return True
    return False

def get_false_pickup_reports():
    reports_list = []
    matches = select_false_pickup_matches()
    for m in matches:
        acc = select_account_by_email(m.lost_item.email)
        archive = select_archive_item_by_match_id(m.id)
        report = {
            "id": str(m.id),
            "owner_fullname": acc.name + " " + acc.surname,
            "pickupby_fullname": + archive.owner_name + " " + archive.owner_surname
        }
        reports_list.append(report)
    return reports_list

# models_list = [cls for name, cls in inspect.getmembers(models, inspect.isclass)
#                if cls != models.Accounts and cls != models.Match]
# archive_models = {
#     models.PersonalItems: ArchivePersonalItems,
#     models.Jewelry: ArchiveJewelry,
#     models.Accessories: ArchiveAccessories,
#     models.TravelItems: ArchiveTravelItems,
#     models.ElectronicDevices: ArchiveElectronicDevices,
#     models.Clothing: ArchiveClothing,
#     models.OfficeItems: ArchiveOfficeItems,
#     models.OtherItems: ArchiveOtherItems
# }
# # TODO Better email verification
# email_regex = r"^[^@]+@[^@]+\.[^@]+$"

# def get_submitted_lost_items(email: str) -> list[Lost_Item]:
#     if re.match(email_regex, email) == None:
#         raise Exception(f"Invalid email address! {email}")

#     models = select_items(email)
#     return_list = []

#     for model in models:
#         item = Lost_Item(
#             category=model.__tablename__,
#             item_type=model.type,
#             desc=model.description,
#             status=model.status,
#             item_id=str(model.id),
#             color=getattr(model, "color", None),
#             size=getattr(model, "size", None),
#             material=getattr(model, "material", None),
#             brand=getattr(model, "brand", None),
#             name=getattr(model, "name", None)
#         )

#         matches = select_matches(model.id, type(model))
#         for match in matches:
#             # TODO Make it so I can use enum here
#             if match.status == "confirmed":
#                 item.status = "confirmed"
#                 break

#         return_list.append(item)

#     return return_list

# def submit_lost_item(email: str, item: Lost_Item):
#     model = create_model_from_item(item.category, item, email)
#     if model == None:
#         raise Exception(f"Invalid item cateogory! {item.category}")
    
#     # TODO Make it so I can use the enum here
#     model.status = "lost"
#     insert_update_item(model)

# def submit_found_item(email: str, item: Found_Item):
#     model = create_model_from_item(item.category, item, email)
#     if model == None:
#         raise Exception(f"Invalid item cateogory! {item.category}")
    
#     # TODO Make it so I can use the enum here
#     model.status = "found"
#     insert_update_item(model)

# # TODO change model_name:str back to model_cls:object
# def delete_lost_item(email: str, id: int, model_name: str):
#     model_cls = None
#     for m in models_list:
#         if m.__tablename__ == model_name:
#             model_cls = m
#     if model_cls == None:
#         return None
    
#     selected = select_item_by_id(id, model_cls)
#     if selected == None:
#         raise Exception(f"{model_cls.__name__} of id {id} does not exist!")
#     if selected.email != email:
#         raise Exception("Attempt to delete item of other user!")
#     delete_item(selected)

# def hand_over_and_archive_match(id: int, model_name: str):
#     model_cls = None
#     for m in models_list:
#         if m.__tablename__ == model_name:
#             model_cls = m
#     if model_cls == None:
#         return None
    
#     f_model = select_item_by_id(id, model_cls)
#     matches = select_matches(id, model_cls)

#     for m in matches:
#         if m.status == MatchStatus.CONFIRMED:
#             l_model = select_item_by_id(m.lost_item_id, model_cls)
#             owner = select_account(l_model.email)

#             data = f_model.dict()
#             data.pop("status")
#             data["email"] = owner.email
#             data["username"] = owner.name
#             data["surname"] = owner.surname
#             data["pesel"] = owner.pesel

#             archive_cls = archive_models[model_cls]
#             archive_model = archive_cls(**data)

#             insert_update_item(archive_model)
#             delete_item(f_model)
#             delete_item(l_model)
#             delete_item(m)
#             break


# def create_model_from_item(model_name: str, item: Item, email: str) -> object:
#     model_cls = None
#     for m in models_list:
#         if m.__tablename__ == model_name:
#             model_cls = m
#     if model_cls == None:
#         return None
    
#     model = model_cls(
#         type=item.item_type,
#         email=email,
#         description=item.desc
#     )
#     if item.color != None and hasattr(model, "color"):
#         model.color = item.color
#     if item.size != None and hasattr(model, "size"):
#         model.size = item.size
#     if item.material != None and hasattr(model, "material"):
#         model.material = item.material
#     if item.brand != None and hasattr(model, "brand"):
#         model.brand = item.brand
#     if item.name != None and hasattr(model, "name"):
#         model.name = item.name

#     return model