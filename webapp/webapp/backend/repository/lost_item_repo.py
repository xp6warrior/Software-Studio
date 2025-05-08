import reflex as rx
import inspect
import webapp.models.models as models

models_list = [cls for name, cls in inspect.getmembers(models, inspect.isclass) if not cls == models.Accounts]

def select_items(email: str) -> list:
    model_list = []

    with rx.session() as session:
        for model_cls in model_list:
            models = session.exec(
                model_cls.select().where(
                    (model_cls.email == email)
                )
            ).all()
            model_list.append(dict(models))
    return model_list

def insert_item(model: object):
    with rx.session() as session:
        session.add(model)
        session.commit()

def update_item(model: object, model_cls: object, id: int, email: str):
    with rx.session() as session:
        item = session.exec(
            model_cls.select().where(
                (model_cls.id == id),
                (model_cls.email == email)
            )
        ).first()
        item = model
        session.add(item)
        session.commit()

def delete_item(model_cls: object, id: int, email: str):
    with rx.session() as session:
        item = session.exec(
            model_cls.select().where(
                (model_cls.id == id),
                (model_cls.email == email)
            )
        ).first()
        session.delete(item)
        session.commit()