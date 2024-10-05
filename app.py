# app.py
import streamlit as st
import threading
from scraper.scrape import scrape_and_store_rss, rss_urls
from database.crud import create_tables, fetch_news
from datetime import datetime, timedelta
import time

# Streamlit cache for fetched news
@st.cache_data(ttl=600)  # Cache news for 10 minutes
def cached_fetch_news(source, start_date, end_date):
    return fetch_news(source, start_date, end_date)

# Function to run scraper periodically (every X minutes or hours)
def start_scraping():
    while True:
        scrape_and_store_rss()  # Scrape and store the latest news
        time.sleep(3600)  # Scrape every 1 hour, adjust as needed

# Start scraper in a separate thread
scraper_thread = threading.Thread(target=start_scraping, daemon=True)
scraper_thread.start()

# Initialize the database and tables
create_tables()

# Streamlit Application
st.title("Live RSS News Feed")

# Dropdown for selecting news source
selected_source = st.selectbox('Select News Channel', list(rss_urls.keys()))

# Date range input from the user
today = datetime.today()
default_start_date = today - timedelta(days=7)
start_date = st.date_input("Start Date", value=default_start_date)
end_date = st.date_input("End Date", value=today)

# Convert Streamlit date input to datetime objects
start_date = datetime.combine(start_date, datetime.min.time())
end_date = datetime.combine(end_date, datetime.min.time())

# Fetch data from the SQLite database based on the filters (cached)
news_items = cached_fetch_news(selected_source, start_date, end_date)

# Show the news in Streamlit
if news_items:
    for news in news_items:
        st.write(f"### {news[0]}")  # title
        st.write(news[1])  # description
        st.write(f"[Read more]({news[2]})")  # link
        st.write(f"Published: {news[3]}")  # published_date
        st.write("---")
else:
    st.write("No news available for this date range.")
