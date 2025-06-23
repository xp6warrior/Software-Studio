from webapp.repository.account_repo import *
from webapp.repository.account_repo import delete_account as delete_account_from_repo

import os
import bcrypt
from email_validator import validate_email, EmailNotValidError
from sqlalchemy.exc import IntegrityError

def create_account(email: str, password: str, role: str, name: str, surname: str) -> str:
    if email == "" or password == "" or role == "" or name == "" or surname == "":
        return "All information is required!"
    
    if " " in email or " " in password or " " in role or " " in name or " " in surname:
        return "Invalid credentials"

    with open(os.getenv("CONFIGS_PATH") + "/config.txt", "r") as f:
        lines = [line.strip() for line in f.readlines()] 
    if lines[2] not in email:
        return f"Email doesn't belong to {lines[0]}"

    # Validate email format
    try:
        validate_email(email)
    except EmailNotValidError:
        return "Invalid email address format!"
    
    # Hash password
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    
    # Insert the account
    try:
        insert_update_account(Accounts(
            email=email, password=hashed_password, role=role, name=name, surname=surname
        ))
        return "Account successfully registered"
    except IntegrityError:
        return "Email address already in use"

def login(email: str, password: str) -> str:
    account = select_account_by_email(email)
    if account == None or not bcrypt.checkpw(password.encode(), account.password.encode()):
        default_admin_user = os.getenv("DEFAULT_ADMIN_USER")
        default_admin_pass = os.getenv("DEFAULT_ADMIN_PASS")
        if default_admin_user is not None and default_admin_pass is not None and default_admin_user == email and default_admin_pass == password:
            return "ADMIN"
        return False
    else:
        return account.role
    
def get_user_account_details(email: str) -> dict[str, str]:
    account = select_account_by_email(email)
    if account == None:
        return False
    else:
        return {
            "name": account.name,
            "surname": account.surname,
            "email": account.email,
            "role": account.role
        }
    
def get_accounts() -> list[dict[str, str]]:
    accounts = select_all_accounts()
    accounts_list = []
    for acc in accounts:
        accounts_list.append({
            "name": acc.name,
            "surname": acc.surname,
            "email": acc.email,
            "role": acc.role
        })
    return accounts_list

def delete_account(email: str) -> bool:
    account = select_account_by_email(email)
    if account == None:
        return False
    else:
        delete_account_from_repo(account)
        return True