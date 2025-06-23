from webapp.repository.account_repo import *
from webapp.models.enums import RoleEnum

def create_user(email: str, password: str, role: RoleEnum, pesel: int, name: str, surname: str):
    insert_update_account(Accounts(
        email=email, password=password, role=role, pesel=pesel, name=name, surname=surname
    ))

def login_user(email: str, password: str) -> RoleEnum:
    account = select_account(email)
    if account == None or account.password != password:
        return None
    else:
        return account.role
    
def get_account_details(email: str) -> dict[str, str]:
    selected = select_account(email)
    return {
        "name": selected.name,
        "surname": selected.surname,
        "email": selected.email,
        "pesel": selected.pesel,
        "role": selected.role
    }