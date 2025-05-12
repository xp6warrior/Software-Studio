from apscheduler.schedulers.blocking import BlockingScheduler
from matching import match_items
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def run_matching_job():
    logging.info("running matching...")
    match_items()
    logging.info("matching completed")

if __name__ == "__main__":
    scheduler = BlockingScheduler(timezone='Europe/Warsaw')

    scheduler.add_job(run_matching_job, 'interval', seconds=10)

    logging.info("Scheduler started. Matching will run at 7AM and 2PM daily.")
    scheduler.start()
