import reflex as rx

from webapp.models2.models import Matches, Items
from webapp.models2.enums import StatusEnum

def select_matches(item: Items, offset: int = 0, limit: int = 10) -> list[Matches]:
    if item == None:
        raise Exception("item must not be None!")
    elif not isinstance(item, Items):
        raise Exception("item must be of type Items!")
    if offset == None or limit == None:
        raise Exception("offset and limit must not be None!")
    elif type(offset) != int or type(offset) != int:
        raise Exception("offset and limit must be of type int!")
    elif offset < 0 or limit < offset:
        raise Exception("offset and limit must be at least 0, and in ascending order!")
    
    with rx.session() as session:
        if item.status == StatusEnum.LOST:
            matches = session.scalars(
                item._lost_matches.select().offset(offset).limit(limit)
            ).all()
        elif item.status == StatusEnum.FOUND:
            matches = session.scalars(
                item._found_matches.select().offset(offset).limit(limit)
            ).all()
    return matches

def insert_update_match(match: Matches):
    if match == None:
        raise Exception("match must not be None!")
    elif type(match) != Matches:
        raise Exception("match must be of type Matches!")

    with rx.session() as session:
        session.add(match)
        session.commit()
        session.refresh(match)