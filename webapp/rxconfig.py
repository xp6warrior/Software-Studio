import reflex as rx
from os import getenv

db_url = getenv("DATABASE_URL")

config = rx.Config(
    app_name="webapp",
    db_url=db_url
)