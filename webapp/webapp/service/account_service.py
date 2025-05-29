from webapp.repository.account_repo import *
from webapp.repository.account_repo import delete_account as remove_acc
from webapp.models.enums import RoleEnum

import secrets
import string
from email_validator import validate_email, EmailNotValidError
from sqlalchemy.exc import IntegrityError

def create_account(email: str, password: str, role: RoleEnum, pesel: int, name: str, surname: str) -> str:
    if type(email) != str or type(role) != RoleEnum or type(pesel) != int or type(name) != str or type(surname) != str:
        return "Error: Parameters have incorrect data types!"
    
    # Validate email format
    try:
        validate_email(email)
    except EmailNotValidError:
        return "Error: Invalid email address!"
    
    # Generate password if none provided
    if password == None:
        chars = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(secrets.choice(chars) for _ in range(14))
    elif type(password) != str:
        return "Error: Parameters have incorrect data types!"
    
    # Insert the account
    try:
        insert_update_account(Accounts(
            email=email, password=password, role=role, pesel=pesel, name=name, surname=surname
        ))
    except IntegrityError:
        return "Error: Email or pesel already used"

def login_user(email: str, password: str) -> RoleEnum:
    account = select_account(email)
    if account == None or account.password != password:
        return False
    else:
        return account.role
    
def get_account_details(email: str) -> dict[str, any]:
    account = select_account(email)
    if account == None:
        return False
    else:
        return {
            "name": account.name,
            "surname": account.surname,
            "email": account.email,
            "pesel": account.pesel,
            "role": account.role
        }
    
def get_accounts() -> list[dict[str, any]]:
    accounts = select_all_accounts()
    accounts_list = []
    for acc in accounts:
        accounts_list.append({
            "name": acc.name,
            "surname": acc.surname,
            "email": acc.email,
            "pesel": acc.pesel,
            "role": acc.role
        })
    return accounts_list

def delete_account(email: str) -> bool:
    account = select_account(email)
    if account == None:
        return False
    else:
        remove_acc(account)
        return True