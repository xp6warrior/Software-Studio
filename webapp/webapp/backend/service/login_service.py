from webapp.backend.repository.login_repo import *
from webapp.models.enums import RoleEnum

"""
    Creates an account object from the parameters, and inserts it into the database.

    Parameters:
        email (str)
        password (str)
        role (RoleEnum)

    Returns:
        Nothing.
"""
def create_user(email: str, password: str, role: RoleEnum):
    account = Accounts(email=email, password=password, role=role)
    insert_account(account)

"""
    Finds an account object in the database, checks if the passwords match and returns it's role.

    Parameters:
        email (str)
        password (str)

    Returns:
        RoleEnum of the account.
"""
def login_user(email: str, password: str) -> RoleEnum:
    account = select_account(email)
    if account.password == password:
        return account.role
    else:
        return None