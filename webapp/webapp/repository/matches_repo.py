import reflex as rx

from webapp.models2.models import Matches, Items
from webapp.models2.enums import StatusEnum

def select_matches(item: Items) -> list[Matches]:
    if item == None:
        raise Exception("item must not be None!")
    elif not isinstance(item, Items):
        raise Exception("item must be of type Items!")
    
    with rx.session() as session:
        if item.status == StatusEnum.LOST:
            matches = session.scalars(
                item._lost_matches.select()
            ).all()
        elif item.status == StatusEnum.FOUND:
            matches = session.scalars(
                item._found_matches.select()
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