from sqlalchemy.orm import Session
from datetime import date, timedelta
from database import SessionLocal
from models.models import Accounts
from models.enums import RoleEnum
from mail.send import send_templated_email
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def run_inactivity_job():
    logging.info("Running LOST item expiry check job...")
    session: Session = SessionLocal()
    try:
        today = date.today()
        warn_date = today - timedelta(days=10)

        accounts = session.query(Accounts).filter(Accounts.role == RoleEnum.WORKER).all()
        for acc in accounts:
            last_login = acc.last_login.date()

            logging.info(f"Last_login {last_login}, warn data {warn_date}")
            if last_login == warn_date:
                logging.info(f"Sending inactivity email for account {acc.email}")
                send_templated_email(
                    to=acc.email,
                    template_id=11,
                    name=acc.name,
                    surname=acc.surname,
                )

        logging.info("Expiry check completed.")
    except Exception as e:
        logging.error(f"Expiry check job failed: {e}")
        session.rollback()
    finally:
        session.close()