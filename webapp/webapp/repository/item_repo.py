import reflex as rx
import inspect
import webapp.models.models as models
from datetime import datetime, timezone

models_list = [cls for name, cls in inspect.getmembers(models, inspect.isclass)
               if cls != models.Accounts and cls != models.Match]

"""
    CRUD model operations.
"""

def select_items(email: str) -> list[rx.Model]:
    if email == None:
        raise Exception("select_items parameter must not be None!")
    elif type(email) != str:
        raise Exception("select_items parameter must be of type str!")
    
    items_list = []
    with rx.session() as session:
        for model_cls in models_list:
            models = session.exec(
                model_cls.select().where(
                    model_cls.email == email
                )
            ).all()
            if models == []: continue
            for m in models:
                items_list.append(m)

        session.commit()
        for i in items_list:
            session.refresh(i)
        
    return items_list

def select_item_by_id(id: int, model_cls: object) -> rx.Model | None:
    if id == None:
        raise Exception("select_item_by_id id must not be None!")
    elif type(id) != int:
        raise Exception("select_item_by_id id must be of type int!")
    
    with rx.session() as session:
        model = session.exec(
            model_cls.select().where(
                model_cls.id == id
            )
        ).first()
        if model != None:
            session.commit()
            session.refresh(model)
    return model

def insert_update_item(model: object):
    if model == None:
        raise Exception("insert_update_item parameter must not be None!")
    elif not isinstance(model, rx.Model):
        raise Exception("insert_update_item parameter must be of type Model!")
    
    model.pickup = datetime.now(timezone.utc)

    with rx.session() as session:
        session.add(model)
        session.commit()
        session.refresh(model)

def delete_item(model: object):
    if model == None:
        raise Exception("delete_item parameter must not be None!")
    elif not isinstance(model, rx.Model):
        raise Exception("delete_item parameter must be of type Model!")
    
    with rx.session() as session:
        session.delete(model)
        session.commit()