import reflex as rx
from sqlalchemy import select, func

from webapp.models2.models import Matches, Items
from webapp.models2.enums import StatusEnum, MatchStatusEnum

def select_matches_by_item(item: Items) -> list[Matches]:
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

def select_match_by_id(match_id: int) -> Matches:
    if match_id == None:
        raise Exception("match_id must not be None!")
    elif not isinstance(match_id, int):
        raise Exception("match_id must be of type int!")
    
    with rx.session() as session:
        match = session.exec(
            select(Matches).where(Matches.id == match_id)
        ).scalars().first()
    return match

def select_match_stats():
    with rx.session() as session:
        results = session.exec(
            select(Matches.status, func.count()).group_by(Matches.status)
        ).all()
    return results

def select_false_pickup_matches() -> list[Matches]:
    with rx.session() as session:
        matches = session.exec(
            select(Matches).where(Matches.status == MatchStatusEnum.FALSE_PICKUP)
        ).scalars().all()
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