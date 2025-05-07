"""EXAMPLE"""

import reflex as rx
from rxconfig import config

from webapp.models.models import Accounts
from webapp.models.enums import RoleEnum

class State(rx.State):
    @rx.event
    def add_account(self):
        with rx.session() as session:
            session.add(
                Accounts(
                    email="abc@gmail.com",
                    password="12345",
                    role=RoleEnum.ADMIN
                )
            )
            session.commit()

def index() -> rx.Component:
    # Welcome Page (Index)
    return rx.center(
        "Email: abc@gmail.com, Password: 12345, Role: admin",
        "Check the DB for proof ex. using DBeaver",
        rx.button(
            "Add this account",
            on_click=State.add_account
        )
    )


app = rx.App()
app.add_page(index)
