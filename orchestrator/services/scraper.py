import time
import logging
import requests
from threading import Thread
from datetime import datetime

from db_stub import get_deployment_profiles, update_host_status, save_deployment_metrics, get_deployment_metrics
from services.db.db_methods import get_deployment_profile

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
        
        for id, profile in profiles.items():
            if profile['deployed']:
                try:
                    hostname = profile['host']['hostname']
                    metrics_url = f"http://{hostname}:5000/metrics"
                    logger.info(f"  Scraping metrics from {metrics_url}...")
                    
                    response = requests.get(metrics_url, timeout=5)
                    response.raise_for_status() # Raise an exception for bad status codes (4xx or 5xx)
                    
                    # Parse and save the metrics
                    metrics_data = response.json()
                    save_deployment_metrics(id, metrics_data)
                    
                    # Update the host's status to UP
                    update_host_status(id, "UP")
                    logger.info(f"  Successfully scraped {hostname}. Status: UP.")     
                    log_last_metrics(id, profile['host']['name'], metrics_data, logger)
                except requests.exceptions.RequestException as e:
                    if profile['status']['state'] == 'UP':
                        update_host_status(id, "DOWN")
                        logger.error(f"  Failed to scrape {hostname}. Status: DOWN. Error: {e}")
        time.sleep(10)

def log_last_metrics(id: int, name: str, metrics: dict, logger: logging.Logger):
    logger.info(f"{name}[CPU% - {metrics['cpu']}% | MEM% - {metrics['mem']}% | DISK% - {metrics['disk']}%]")         