from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import date, timedelta
from database import SessionLocal
from models.models import Items, Matches, StatusEnum, Accounts
from mail.send import send_templated_email
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def run_expiry_check_job():
    logging.info("Running LOST item expiry check job...")
    session: Session = SessionLocal()
    try:
        today = date.today()
        warn_date = today - timedelta(days=25)
        delete_date = today - timedelta(days=30)

        lost_items = session.query(Items).filter(Items.status == StatusEnum.LOST).all()

        for item in lost_items:
            created_date = item.created_at.date()

            # Find associated account
            account = session.query(Accounts).filter_by(email=item.email).first()
            if not account:
                logging.warning(f"No account found for item ID {item.id}, email: {item.email}")
                continue

            if created_date == warn_date:
                logging.info(f"Sending warning email (25d) for item ID {item.id}")
                send_templated_email(
                    to=account.email,
                    template_id=6,
                    name=account.name,
                    surname=account.surname,
                    item_id=item.id
                )

            elif created_date == delete_date:
                logging.info(f"Sending deletion email (30d) and deleting item ID {item.id}")
                send_templated_email(
                    to=account.email,
                    template_id=7,
                    name=account.name,
                    surname=account.surname,
                    item_id=item.id
                )

                session.query(Matches).filter(
                    (Matches.lost_item_id == item.id) | (Matches.found_item_id == item.id)
                ).delete(synchronize_session=False)

                session.delete(item)

        session.commit()
        logging.info("Expiry check completed.")
    except Exception as e:
        logging.error(f"Expiry check job failed: {e}")
        session.rollback()
    finally:
        session.close()
