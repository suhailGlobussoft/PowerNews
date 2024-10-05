# app.py
import streamlit as st
import threading
from scraper.scrape import scrape_and_store_rss,rss_urls
from database.crud import create_tables, fetch_news
from datetime import datetime, timedelta

# Function to run scraper periodically (every X minutes or hours)
def start_scraping():
    scrape_and_store_rss()
    # You can use a scheduling library like schedule for periodic scraping.

# Start scraper in a separate thread
scraper_thread = threading.Thread(target=start_scraping)
scraper_thread.start()

# Initialize the database and tables
create_tables()

# Streamlit Application
st.title("Live RSS News Feed")

# Dropdown for selecting news source

selected_source = st.selectbox('Select News Channel', list(rss_urls.keys()))


# Date input from the user
start_date = st.date_input("Start Date", value=datetime.today())
end_date = st.date_input("End Date", value=datetime.today())

# Convert Streamlit date input to datetime objects
start_date = datetime.combine(start_date, datetime.min.time())
end_date = datetime.combine(end_date, datetime.min.time())

# Fetch data from the SQLite database based on the filters
news_items = fetch_news(selected_source, start_date, end_date)

print(news_items)
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
