import reflex as rx
from sqlalchemy import select

from webapp.models2.models import Accounts

"""
    CRUD account operations.
"""

def select_account(email: str) -> Accounts | None:
    if email == None:
        raise Exception("select_account_by_email parameter must not be None!")
    elif type(email) != str:
        raise Exception("select_account_by_email parameter must be of type str!")
    
    with rx.session() as session:
        account = session.exec(
            select(Accounts).where(
                Accounts.email == email
            )
        ).scalars().first()
        if account == None:
            return None
    return account

def select_all_accounts() -> list[Accounts]:
    with rx.session() as session:
        accounts = session.exec(select(Accounts)).scalars().all()
    return accounts
    
def insert_update_account(account: Accounts):
    if account == None:
        raise Exception("insert_update_account parameter must not be None!")
    elif type(account) != Accounts:
        raise Exception("insert_update_account parameter must be of type Accounts!")
    
    with rx.session() as session:
        session.add(account)
        session.commit()
        session.refresh(account)

def delete_account(account: Accounts):
    if account == None:
        raise Exception("delete_account parameter must not be None!")
    elif type(account) != Accounts:
        raise Exception("delete_account parameter must be of type Accounts!")
    
    with rx.session() as session:
        session.delete(account)
        session.commit()