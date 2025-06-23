import reflex as rx
from sqlalchemy import select

from webapp.models2.models import Items

"""
    CRUD model operations.
"""

def select_items_by_email(email: str) -> list[Items]:
    if email == None:
        raise Exception("select_items_by_email parameter must not be None!")
    elif type(email) != str:
        raise Exception("select_items_by_email parameter must be of type str!")
    
    with rx.session() as session:
        items = session.exec(
            select(Items).where(Items.email == email)
        ).scalars().all()
        for i in items:
            session.refresh(i)
    return items

# def select_item_by_id(id: int, model_cls: object) -> rx.Model | None:
#     if id == None:
#         raise Exception("select_item_by_id id must not be None!")
#     elif type(id) != int:
#         raise Exception("select_item_by_id id must be of type int!")
    
#     with rx.session() as session:
#         model = session.exec(
#             model_cls.select().where(
#                 model_cls.id == id
#             )
#         ).first()
#         if model != None:
#             session.commit()
#             session.refresh(model)
#     return model

def insert_update_item(item: Items):
    if item == None:
        raise Exception("insert_update_item parameter must not be None!")
    elif not isinstance(item, Items):
        raise Exception("insert_update_item parameter must be of type Items!")

    with rx.session() as session:
        session.add(item)
        session.commit()
        session.refresh(item)

def delete_item(item_id: int):
    if item_id == None:
        raise Exception("delete_item parameter must not be None!")
    elif not isinstance(item_id, int):
        raise Exception("delete_item parameter must be of type int!")
    
    with rx.session() as session:
        item = session.exec(select(Items).where(Items.id == item_id)).scalars().first()
        session.delete(item)
        session.commit()