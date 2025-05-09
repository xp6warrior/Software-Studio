import inspect
import re
import webapp.models.models as models
import webapp.models.enums as enums
from webapp.backend.repository.item_repo import *

models_list = [cls for name, cls in inspect.getmembers(models, inspect.isclass) if not cls == models.Accounts]
email_regex = r"^[^@]+@[^@]+\.[^@]+$"

"""
    Gets a list of all models belonging to the user.

    Parameters:
        email (str): The email (primary key) of the account.
    
    Returns:
        A list of models belonging to the user.
"""
def get_submitted_items(email: str) -> list[rx.Model]:
    models = select_items_by_email(email)
    formatted_list = []

    for m in models:
        model_columns = {c.name: getattr(m, c.name) for c in m.__table__.columns
                         if c.name != "status" and c.name != "email"}
        formatted_list.append({
            "Item": model_columns,
            "status": m.status
        })
    
    return formatted_list

"""
    Submit item functions:
        submit_lost_item(input_json: dict[str, str])
        submit_found_item(input_json: dict[str, str])

    These functions vertify parameters in input_json, create a model object from
    the parameters, and adds the object into the database.

    The input_json:
        - Requires a "model" attribute, specifying which model class to instantiate
        - Ignores attributes that aren't defined in the model class
        - Ignores the "id" attribute, since this function creates a new entry
        - Status attribute is optional (hardcoded to LOST or FOUND)

    Parameters:
        input_json (dict[str, str]): A json dictionary representing the lost item
        Format:
            {
                "model": "<name_of_model_class>",
                "attribute1": "value",
                "attribute2": "value",
                ...
            }
        The keys are case insensitive!
        The order of the attributes doesn't matter!

    Returns:
        Nothing

    Exception:
        If model is not specified or incorrect.
        If the email doesn't follow the correct email format.
        If the model doesn't fit the database (violates data integrity).
"""
def submit_lost_item(input_json: dict[str, str]):
    model = create_new_model_from_json(input_json)
    model.status = enums.StatusEnum.LOST.value
    insert_update_item(model)

def submit_found_item(input_json: dict[str, str]):
    model = create_new_model_from_json(input_json)
    model.status = enums.StatusEnum.FOUND.value
    insert_update_item(model)

"""
    This functions find the model in the database (based on id and email), modify
    its attributes based on attributes in input_json, and commits the changes to the DB.

    Takes the id (primary key) of an item andd the edited json input of a submitted item,
    edits the model object from the db and commits the changes

    The input_json:
        - Requires a "model" attribute, specifying which model class to instantiate
        - Ignores attributes that aren't defined in the model class
        - Ignores the "id", "email" attributes, since updating those values would be bad

    Parameters:
        input_json (dict[str, str]): A json dictionary representing the lost item
        Format:
            {
                "model": "<name_of_model_class>",
                "attribute1": "value",
                "attribute2": "value",
                ...
            }
        The keys are case insensitive!
        The order of the attributes doesn't matter!

    Returns:
        Nothing

    Exception:
        If the model attribute is not specified or incorrect.
"""
def edit_submitted_item(input_json: dict[str, str]):
    model = select_item_by_id_email(input_json["id"], input_json["email"], input_json["model"])
    for key, val in input_json.items():
        if hasattr(model, key) and key != "status":
            setattr(model, key, val)
    
    insert_update_item(model)

"""
    Takes the id (primary key) of an item, the owner's email and the model of the item. Deletes
    the entry from the database.

    Parameters:
        id (int): The id (primary key) of the item
        email (str): The email (primary key) of the account
        model_name (str): The name of of model (case sensitive!)

    Returns:
        Nothing

    Exception:
        If model_name is incorrect.
"""
def delete_submitted_item(id: int, email: str, model_name: str):
    model = get_model_class(model_name)
    if model == None:
        raise Exception(f"Invalid model class! {model_name}")
    delete_item(get_model_class(model_name), id, email)


def get_model_class(model_name: str) -> object:
    model_cls = None
    for m in models_list:
        if m.__tablename__ == model_name:
            model_cls = m
    return model_cls

def create_new_model_from_json(input_json: dict[str, str]) -> rx.Model:
    # All keys, values to lower case (case insensitive)
    input_json = {key.lower(): val for key, val in input_json.items()}

    # Check for correct email
    if re.match(email_regex, input_json["email"]) == None:
        raise Exception("Email must be valid")
    
    # Find model value
    model_name = input_json.get("model")
    if model_name == None:
        raise Exception("\"model\" attribute must be defined!")
    
    # Find corresponding model class
    model_cls = get_model_class(model_name)
    if model_cls == None:
        raise Exception(f"Invalid model class! {model_name}")
    
    # Create instance of model_cls only with values of only its defined attributes specified
    model_columns = {col.name for col in model_cls.__table__.columns if col.name != "id"}
    model_column_values = {key: val for key, val in input_json.items() if key in model_columns}
    return model_cls(**model_column_values)
