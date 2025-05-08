from sqlmodel import Session, select
from webapp.models import models
from webapp.backend.db import engine
import inspect

# items that can be matched 
models_list = [
    cls for name, cls in inspect.getmembers(models, inspect.isclass)
    if issubclass(cls, models.rx.Model) and cls not in [models.Accounts]
]

def get_model_class_by_name(model_name: str):
    #returns the class of some model we choose
    for cls in models_list:
        if cls.__name__.lower() == model_name.lower():
            return cls
    return None

def get_item_by_id(model_name: str, item_id: int):
    #get the single item by model and items ID
    model_cls = get_model_class_by_name(model_name)
    if model_cls is None:
        raise ValueError(f"Invalid model name: {model_name}")
    with Session(engine) as session:
        statement = select(model_cls).where(model_cls.id == item_id)
        result = session.exec(statement).first()
        return result

def get_all_items_of_model(model_name: str):
    #getting all items of a chosen model
    model_cls = get_model_class_by_name(model_name)
    if model_cls is None:
        raise ValueError(f"Invalid model name: {model_name}")
    with Session(engine) as session:
        statement = select(model_cls)
        results = session.exec(statement).all()
        return results
