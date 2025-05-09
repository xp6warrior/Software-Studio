import reflex as rx
import inspect
import webapp.models.models as models

models_list = [cls for name, cls in inspect.getmembers(models, inspect.isclass) if not cls == models.Accounts]

"""
    CRUD operations for items

    select_items(email: str) -> list:
        Returns a list of models objects in the DB that belong to the account (email).

    insert_updateitem(model: object):
        If the model object doesn't exist in the db yet, it inserts it.
        If the model object does exist (id), it updates that entry.

    delete_item(model: object):
        Deletes the model object from the database.
    
    Exceptions:
        Any data integrity violations will result in an exception thrown by sqlalchemy.
"""

def select_items_by_email(email: str) -> list[rx.Model]:
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

def select_item_by_id_email(id: int, email: str, model_cls: object) -> rx.Model | None:
    with rx.session() as session:
        model = session.exec(
            model_cls.select().where(
                model_cls.id == id,
                model_cls.email == email
            )
        ).first()
        if model != None:
            session.commit()
            session.refresh(model)
    return model

def insert_update_item(model: object):
    with rx.session() as session:
        session.add(model)
        session.commit()
        session.refresh(model)

def delete_item(model: object):
    with rx.session() as session:
        session.delete(model)
        session.commit()