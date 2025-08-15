import time
import logging
import requests
from threading import Thread
from services.alerter import Alerter
from services.db.db_methods import get_deployment_profiles, update_host_status, save_deployment_metrics
from config import SMTP_SERVER, SMTP_PORT, SMTP_USER, SMTP_PASS, RECIPIENT_EMAIL

SCRAPING_INTERVAL = 10  # seconds
alerter = Alerter(SMTP_SERVER, SMTP_PORT, SMTP_USER, SMTP_PASS, RECIPIENT_EMAIL )

def init_scraper():
    thread = Thread(target=scrape_metrics_job, daemon=True)
    thread.start()
    print("Monitoring pull-daemon started successfully")

def conf_scraper_logger():
    logger = logging.getLogger('scraper')
    logger.setLevel(logging.INFO)
    fh = logging.FileHandler("logs/scraper.log")
    format = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    fh.setFormatter(format)
    logger.addHandler(fh)
    return logger

def scrape_metrics_job():
    logger = conf_scraper_logger()
    while True:
        # Fetch the list of hosts from the database
        profiles = get_deployment_profiles()
        
        for profile in profiles:
            if profile['is_deployed']:
                try:
                    hostname = profile['hostname']
                    status_id = profile['status_id']

                    if profile['state'] != 'UP':
                        status_url = f"http://{hostname}:5000/status"
                        logger.info(f"  Scraping status from {status_url}...")
                        response = requests.get(status_url, timeout=5)
                        response.raise_for_status() # Raise an exception for bad status codes (4xx or 5xx)
                        update_host_status(status_id, "UP", response.json())

                    metrics_url = f"http://{hostname}:5000/metrics"
                    logger.info(f"  Scraping metrics from {metrics_url}...")
                    
                    response = requests.get(metrics_url, timeout=5)
                    response.raise_for_status() # Raise an exception for bad status codes (4xx or 5xx)
                    
                    # Parse and save the metrics
                    metrics_data = response.json()
                    save_deployment_metrics(profile['remote_id'], metrics_data)

                    # Run alerter to check thresholds and send alerts if necessary
                    new_status = alerter.check_and_alert(profile, metrics_data)
                                        
                    logger.info(f"Successfully scraped {hostname}. Status: {new_status}.")     
                    log_last_metrics(profile['name'], metrics_data, logger)
                except requests.exceptions.RequestException as e:
                    if profile['state'] != 'DOWN':
                        update_host_status(status_id, "DOWN", None)
                        logger.error(f"  Failed to scrape {hostname}. Status: DOWN. Error: {e}")
        time.sleep(SCRAPING_INTERVAL)

def log_last_metrics(name: str, metrics: dict, logger: logging.Logger):
    logger.info(f"{name}[CPU% - {metrics['cpu']}% | MEM% - {metrics['mem']}% | DISK% - {metrics['disk']}%]")         