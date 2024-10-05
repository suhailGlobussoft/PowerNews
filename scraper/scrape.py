# scraper/scrape.py
import feedparser
from datetime import datetime
from database.crud import insert_rss_feed,check_duplicate

rss_urls = {
    # India
    "The Hindu": "https://www.thehindu.com/feeder/default.rss",
    "NDTV": "https://feeds.feedburner.com/ndtvnews-top-stories",
    "Times of India": "https://timesofindia.indiatimes.com/rssfeedstopstories.cms",
    "Hindustan Times": "https://www.hindustantimes.com/feeds/rss/web-stories/trending/rssfeed.xml",
    "The Economic Times": "https://economictimes.indiatimes.com/rssfeedstopstories.cms",
    "Business Standard": "https://www.business-standard.com/rss/",
    "Mint": "https://www.livemint.com/rss/AI",
    "MediaNama": "https://medianama.com/feed/",
    "Inc42": "https://inc42.com/feed/",
    "ESPN Cricinfo (Cricket)": "https://www.espncricinfo.com/rss/feeds/home.xml",
    "The Indian Express (Sports)": "https://indianexpress.com/section/sports/rss/",
    # International
    "The Guardian": "https://www.theguardian.com/rss",
    "The Wall Street Journal": "https://www.wsj.com/xml/rss/article/WSJnews-world.xml",
    "Bloomberg": "https://www.bloomberg.com/feeds/news",
    "Financial Times": "https://www.ft.com/rss/world-news",
    "The Verge": "https://www.theverge.com/rss",
    "Engadget": "https://www.engadget.com/rss.xml",
    "Science Magazine": "https://www.sciencemag.org/rss",
    "National Geographic": "https://www.nationalgeographic.com/news/rss",
    "Scientific American": "https://www.scientificamerican.com/rss/feed",
    'BBC': 'http://feeds.bbci.co.uk/news/rss.xml',
    'CNN': 'http://rss.cnn.com/rss/cnn_topstories.rss',
    'Al Jazeera': 'https://www.aljazeera.com/xml/rss/all.xml',
    "BBC News": "https://feeds.bbci.co.uk/news/rss.xml",
    "CNN Top Stories": "http://rss.cnn.com/rss/cnn_topstories.rss",
    "Reuters World News": "http://feeds.reuters.com/reuters/worldNews",
    "NY Times World News": "https://rss.nytimes.com/services/xml/rss/nyt/World.xml",
    "TechCrunch": "http://feeds.feedburner.com/TechCrunch/",
    "Google News (Technology)": "https://news.google.com/rss/search?q=technology&hl=en-US&gl=US&ceid=US:en"
}


def scrape_and_store_rss():
    """Function to scrape RSS feeds and store the results in the database"""
    for source, url in rss_urls.items():
        feed = feedparser.parse(url)
        for entry in feed.entries:
            # Prepare data for insertion
            title = entry.title
            description = entry.description if 'description' in entry else ''
            link = entry.link

            # Parse and normalize the date format
            try:
                published_date = datetime.strptime(entry.published, '%a, %d %b %Y %H:%M:%S %Z')
                published_date = published_date.strftime('%Y-%m-%d %H:%M:%S')
            except Exception:
                published_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            # print(f"\n\n {title},{description},{link},{published_date} \n\n")
             # Check if the article already exists in the database
            if not check_duplicate(title, published_date):
                # Insert into the database if no duplicate is found
                insert_rss_feed(title, description, link, published_date, source)
            else:
                print(f"Skipping duplicate: {title} on {published_date}")
           

    print("Scraping and storing complete.")

# scrape_and_store_rss()s
