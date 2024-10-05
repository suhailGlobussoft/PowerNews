import streamlit as st
import threading
from scraper.scrape import scrape_and_store_rss, rss_urls
from database.crud import create_tables, fetch_news
from datetime import datetime, timedelta
import time

# Streamlit cache for fetched news with a TTL of 30 minutes
@st.cache_data(ttl=1800)
def cached_fetch_news(source, start_date, end_date):
    return fetch_news(source, start_date, end_date)

# Function to run the scraper periodically (every X hours)
def start_scraping():
    while True:
        scrape_and_store_rss()  # Scrape and store the latest news
        time.sleep(3600 * 2)  # Scrape every 2 hours

# Start scraper in a separate thread (daemon=True ensures it runs in the background)
scraper_thread = threading.Thread(target=start_scraping, daemon=True)
scraper_thread.start()

# Initialize the database and tables
create_tables()

# Streamlit Application
st.title("Live RSS News Feed")

# Store selected source and date range in session state to avoid recomputation
if 'selected_source' not in st.session_state:
    st.session_state.selected_source = st.selectbox('Select News Channel', list(rss_urls.keys()))
else:
    st.selectbox('Select News Channel', list(rss_urls.keys()), index=list(rss_urls.keys()).index(st.session_state.selected_source))

# Date range input from the user
today = datetime.today()
default_start_date = today - timedelta(days=7)

if 'start_date' not in st.session_state:
    st.session_state.start_date = st.date_input("Start Date", value=default_start_date)
else:
    st.date_input("Start Date", value=st.session_state.start_date)

if 'end_date' not in st.session_state:
    st.session_state.end_date = st.date_input("End Date", value=today)
else:
    st.date_input("End Date", value=st.session_state.end_date)

# Convert Streamlit date input to datetime objects
start_date = datetime.combine(st.session_state.start_date, datetime.min.time())
end_date = datetime.combine(st.session_state.end_date, datetime.min.time())

# Pagination function to display only a subset of the news at a time
def paginate_news(news_items, page_size=10):
    total_pages = (len(news_items) + page_size - 1) // page_size
    page = st.number_input("Page", min_value=1, max_value=total_pages, step=1, key="page_number")
    start_idx = (page - 1) * page_size
    end_idx = start_idx + page_size
    return news_items[start_idx:end_idx]

# Fetch and display news with a spinner for better UX
with st.spinner('Fetching news...'):
    news_items = cached_fetch_news(st.session_state.selected_source, start_date, end_date)

# Paginate and show the news
if news_items:
    paginated_news = paginate_news(news_items)
    for news in paginated_news:
        st.write(f"### {news[0]}")  # title
        st.write(news[1])  # description
        st.write(f"[Read more]({news[2]})")  # link
        st.write(f"Published: {news[3]}")  # published_date
        st.write("---")
else:
    st.write("No news available for this date range.")
