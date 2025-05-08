import inspect
import webapp.models.models as models
from webapp.backend.repository.item_repo import *

models_list = [cls for name, cls in inspect.getmembers(models, inspect.isclass) if not cls == models.Accounts]

"""
    Gets a list of all models belonging to the user.

    Parameters:
        email (str): The email (primary key) of the account.
    
    Returns:
        A list of models belonging to the user.
"""
def get_submitted_lost_items(email: str) -> list[rx.Model]:
    models = select_items(email)
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
    Takes the email of an account and json input of a submitted item, creates a model object
    and inserts it into the database.

    The "model" attribute specifies which model class to instantiate, then the values of all attributes that are defined
    in that table are set. Values of attributes that aren't defined in the model class are ignored.

    Parameters:
        email (str): The email (primary key) of the user
        input_json (dict[str, str]): A json dictionary representing the lost item (without id)
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
        If the model doesn't fit the database (violates data integrity)
"""
def submit_lost_item(email: str, input_json: dict[str, str]):
    input_json["email"] = email
    model = create_model_from_json(input_json)
    insert_update_item(model)

"""
    Takes the id (primary key) of an item, the owner's email and the edited json input of a submitted item,
    edits the model object from the db and commits the changes

    The "model" attribute specifies which model class to instantiate.
    Values of attributes that aren't defined in the model class are ignored.

    Parameters:
        id (int): The id (primary key) of the item
        email (str): The email (primary key) of the user
        input_json (dict[str, str]): A json dictionary representing the lost item (without id)
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
def edit_submitted_lost_item(id: int, email: str, input_json: dict[str, str]):
    input_json["email"] = email
    model = create_model_from_json(input_json)
    model.id = id
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
def delete_submitted_lost_item(id: int, email: str, model_name: str):
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

def create_model_from_json(input_json: dict[str, str]) -> rx.Model:
    # All keys, values to lower case (case insensitive)
    input_json = {key.lower(): val for key, val in input_json.items()}
    
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
