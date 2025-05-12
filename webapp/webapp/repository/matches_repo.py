import reflex as rx
from webapp.models.models import Match
from webapp.models.enums import MatchStatus

# TODO improve these functions

def select_matches(found_id: int, model_cls: object) -> list[rx.Model]:
    if found_id == None:
        raise Exception("select_matches found_id must not be None!")
    elif type(found_id) != int:
        raise Exception("select_matches found_id must be of type int!")
    
    with rx.session() as session:
        matches = session.exec(
            Match.select().where(
                Match.table_name == model_cls.__tablename__,
                Match.found_item_id == found_id
            )
        ).all()
        session.commit()
        for m in matches:
            session.refresh(m)
    return matches

def insert_update_match(match: Match):
    if match == None:
        raise Exception("insert_update_match parameter must not be None!")
    elif type(match) != Match:
        raise Exception("insert_update_match parameter must be of type Match!")

    with rx.session() as session:
        session.add(match)
        session.commit()
        session.refresh(match)