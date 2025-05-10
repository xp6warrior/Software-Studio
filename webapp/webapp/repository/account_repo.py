import reflex as rx
from webapp.models.models import Accounts

"""
    CRUD account operations.
"""

def select_account(email: str) -> Accounts | None:
    if email == None:
        raise Exception("select_account parameter must not be None!")
    elif type(email) != str:
        raise Exception("select_account parameter must be of type str!")
    
    with rx.session() as session:
        account = session.exec(
            Accounts.select().where(
                Accounts.email == email
            )
        ).first()
        session.commit()
        if account == None:
            return None
        session.refresh(account)
    return account

def select_all_accounts() -> list[Accounts]:
    with rx.session() as session:
        accounts = session.exec(
            Accounts.select()
        ).all()
        session.commit()
        for a in accounts:
            session.refresh(a)
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