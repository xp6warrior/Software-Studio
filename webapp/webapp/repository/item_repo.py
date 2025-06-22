import reflex as rx
from sqlalchemy import select, func

from webapp.models2.models import Items, Matches, ArchivedItems
from webapp.models2.enums import StatusEnum

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

def select_item_by_id(id: int) -> Items | None:
    if id == None:
        raise Exception("select_item_by_id id must not be None!")
    elif type(id) != int:
        raise Exception("select_item_by_id id must be of type int!")
    
    with rx.session() as session:
        item = session.exec(
            select(Items).where(Items.id == id)
        ).scalars().first()
        if item != None:
            session.refresh(item)
    return item

def select_archive_item_by_match_id(match_id: int) -> ArchivedItems:
    with rx.session() as session:
        item = session.exec(
            select(ArchivedItems).where(ArchivedItems.match_id == match_id)
        ).scalars().first()
        if item != None:
            session.refresh(item)
    return item

def select_item_stats():
    with rx.session() as session:
        results = session.exec(
            select(Items.status, func.count()).group_by(Items.status)
        ).all()
    return results

def select_num_of_archived_items():
    with rx.session() as session:
        result = session.exec(
            select(func.count()).select_from(ArchivedItems)
        ).scalar_one()
    return result

def insert_update_item(item: Items):
    if item == None:
        raise Exception("insert_update_item parameter must not be None!")
    elif not isinstance(item, Items) and not isinstance(item, ArchivedItems):
        raise Exception("insert_update_item parameter must be of type Items or ArchivedItems!")

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