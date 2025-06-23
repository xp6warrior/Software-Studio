from apscheduler.schedulers.blocking import BlockingScheduler
from matching import match_items
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

    # Run the job every 10 seconds
    scheduler.add_job(run_matching_job, 'interval', seconds=10)
    scheduler.add_job(run_expiry_check_job, 'interval', minutes=2)

    logging.info("Scheduler started. Matching will run at 7AM and 2PM daily.")
    scheduler.start()
