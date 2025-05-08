import reflex as rx
from webapp.models.models import Accounts

"""
    Select and insert account functions. Pretty self-explanitory.
"""

def select_account(email: str) -> Accounts:
    with rx.session() as session:
        account = session.exec(
            Accounts.select().where(
                Accounts.email == email
            )
        ).first()
        session.commit()
        session.refresh(account)
    return account
    
def insert_account(account: object):
    with rx.session() as session:
        session.add(account)
        session.commit()
        session.refresh(account)