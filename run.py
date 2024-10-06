import schedule
import time
import json
import os
from datetime import datetime
from main import scrape_all_feeds  # Assuming the scraper function is in rss_scraper.py

# Directory where JSON files are stored
JSON_DIR = "rss_feeds_data"

# Scraper task that runs the RSS feed scraping process
def run_scraper_task():
    print(f"Scraping started at {datetime.now()}")
    
    # Assuming you have a scraper function that scrapes all feeds by categories
    # and stores them in the `rss_feeds_data` directory.
    scrape_all_feeds(JSON_DIR)
    
    print(f"Scraping completed at {datetime.now()}")


schedule.every(30).minutes.do(run_scraper_task)
# Scheduler setup: run the scraper task every hour
# schedule.every(1).hour.do(run_scraper_task)

# You can change this to:
# schedule.every().day.at("00:00").do(run_scraper_task)  # Daily at midnight
# schedule.every(30).minutes.do(run_scraper_task)         # Every 30 minutes
# schedule.every().monday.do(run_scraper_task)            # Every Monday
# schedule.every().wednesday.at("13:15").do(run_scraper_task) # Every Wednesday at 13:15

# Main loop to keep the scheduler running
if __name__ == "__main__":
    print("Scheduler started")
    while True:
        schedule.run_pending()  # Run scheduled tasks
        time.sleep(1)  # Wait for 1 second before checking again
