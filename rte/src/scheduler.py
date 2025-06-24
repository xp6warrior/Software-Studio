from apscheduler.schedulers.blocking import BlockingScheduler
from automaticdeletion import run_expiry_check_job
from matching import match_all_lost_and_found
from inactivity import run_inactivity_job
from database import SessionLocal
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def run_matching_job():
    logging.info("Running matching job...")
    session = SessionLocal()
    try:
        match_all_lost_and_found(session)
        logging.info("Matching completed.")
    except Exception as e:
        logging.error(f"Matching job failed: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    scheduler = BlockingScheduler(timezone='Europe/Warsaw')

    scheduler.add_job(run_matching_job, 'interval', seconds=30)
    scheduler.add_job(run_expiry_check_job, 'interval', seconds=30)
    scheduler.add_job(run_inactivity_job, 'interval', seconds=30)

    logging.info("Combined scheduler started.")
    scheduler.start()
