from sqlalchemy.orm import Session
from sqlalchemy.inspection import inspect
from models.models import Match
from models import models
from models import enums
from db import SessionLocal
import logging

MATCH_THRESHOLDS = {
    models.PersonalItems: 1,
    models.Jewelry: 2,
    models.Accessories: 3,
    models.TravelItems: 3,
    models.ElectronicDevices: 3,
    models.Clothing: 3,
    models.OfficeItems: 2,
    models.OtherItems: 3,
}

EXCLUDED_COLUMNS = {'id', 'status', 'email', 'description'} #these attributes are useless for matching so we skip them

MATCH_CONFIG = {}
for model_cls, threshold in MATCH_THRESHOLDS.items():
    columns = [c.key for c in inspect(model_cls).columns if c.key not in EXCLUDED_COLUMNS]
    MATCH_CONFIG[model_cls] = (columns, threshold)

def get_relevant_items(session: Session, model_cls, status):
    return session.query(model_cls).filter(model_cls.status == status).all()

def calculate_match_percentage(attrs, item1, item2):
    #returns the percentage of match
    total = len(attrs)
    if total == 0:
        return 0
    matches = sum(getattr(item1, attr) == getattr(item2, attr) for attr in attrs)
    return int((matches / total) * 100)

def match_items():
    session = SessionLocal()

    for model_cls, (attrs, threshold) in MATCH_CONFIG.items():
        table_name = model_cls.__tablename__

        lost_items = get_relevant_items(session, model_cls, enums.StatusEnum.LOST)
        found_items = get_relevant_items(session, model_cls, enums.StatusEnum.FOUND)

        for lost in lost_items:
            for found in found_items:
                # skip if already matched
                existing_match = session.query(Match).filter_by(
                    table_name=table_name,
                    lost_item_id=lost.id,
                    found_item_id=found.id
                ).first()
                if existing_match:
                    continue

                percentage = calculate_match_percentage(attrs, lost, found)

                if percentage == 0:
                    continue  # skip useless matches

                if percentage >= (threshold / len(attrs)) * 100:
                    new_match = Match(
                        table_name=table_name,
                        lost_item_id=lost.id,
                        found_item_id=found.id,
                        status=enums.MatchStatus.UNCONFIRMED,
                        percentage=percentage
                    )
                    # TODO Fix the error type mismatch error between db and model class
                    # Move commit to the end of the function to recreate
                    session.add(new_match)
                    session.commit()

    session.close()

def get_stats():
    session = SessionLocal()
    total_lost = total_found = 0

    for model_cls in MATCH_CONFIG.keys():
        total_lost += session.query(model_cls).filter(model_cls.status == 'lost').count()
        total_found += session.query(model_cls).filter(model_cls.status == 'found').count()

    unconfirmed_matches = session.query(Match).filter(Match.status == enums.MatchStatus.UNCONFIRMED).count()
    confirmed_matches = session.query(Match).filter(Match.status == enums.MatchStatus.CONFIRMED).count()

    session.close()
    return [
        {"Number of lost items": total_lost, "Number of found items": total_found},
        {"Number of unconfirmed matches": unconfirmed_matches, "Number of confirmed matches": confirmed_matches}
    ]
