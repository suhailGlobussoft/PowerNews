import feedparser
import json
import os
from datetime import datetime

# Directory where JSON files will be saved
OUTPUT_DIR = "rss_feeds_data"
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

# Function to load existing JSON data or initialize an empty list if the file does not exist
def load_existing_data(category):
    file_path = os.path.join(OUTPUT_DIR, f"{category.lower()}.json")
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    return []

# Function to save data back to JSON file
def save_data(category, data):
    file_path = os.path.join(OUTPUT_DIR, f"{category.lower()}.json")
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

# Function to scrape and store RSS feeds
def parse_and_store_feed(feed_url, category, source):
    feed = feedparser.parse(feed_url)
    existing_data = load_existing_data(category)
    existing_links = {item['link'] for item in existing_data}

    new_items = []
    for entry in feed.entries:
        if entry.link not in existing_links:
            # Prepare the feed item as a dictionary
            feed_item = {
                'title': entry.title,
                'link': entry.link,
                'description': entry.get('description', ''),
                'published': entry.get('published', ''),
                'category': category,
                'scraped_at': datetime.now().isoformat(),  # Timestamp when scraped
                'source': source  # Include the source of the feed
            }
            new_items.append(feed_item)
            existing_data.append(feed_item)  # Add the new item to the existing data

    if new_items:
        save_data(category, existing_data)
        print(f"Added {len(new_items)} new items to {category}.json")
    else:
        print(f"No new items found for {category}")

# Function to scrape all categories
def scrape_all_feeds(feed_urls):
    for category, feeds in feed_urls.items():
        print(f"Scraping category: {category}")
        for feed in feeds:
            url = feed['rssFeedUrl']
            source = feed['source']
            parse_and_store_feed(url, category, source)

if __name__ == "__main__":
    # Dictionary of feed URLs mapped to their category names
    feed_urls = {
        "Top Stories": [
            {"rssFeedUrl":"https://feeds.feedburner.com/ndtvnews-top-stories", "source":"NDTV"},
            {"rssFeedUrl":"https://feeds.feedburner.com/ndtvnews-trending-news", "source":"NDTV"},
            {"rssFeedUrl":"https://frontline.thehindu.com/feeder/default.rss", "source":"The Hindu"},
            {"rssFeedUrl":"https://timesofindia.indiatimes.com/rssfeedstopstories.cms", "source":"Times of India"},
            {"rssFeedUrl":"https://timesofindia.indiatimes.com/rssfeedmostrecent.cms", "source":"Times of India"},
            {"rssFeedUrl":"https://economictimes.indiatimes.com/rssfeedstopstories.cms", "source":"Economic Times"},
            
            {"rssFeedUrl":"http://rss.cnn.com/rss/money_topstories.rss", "source":"CNN"},  
            {"rssFeedUrl":"http://rss.cnn.com/rss/money_mostpopular.rss", "source":"CNN"},
            {"rssFeedUrl":"https://www.aljazeera.com/xml/rss/all.xml", "source":"Al Jazeera"},
            {"rssFeedUrl":"https://feeds.bbci.co.uk/news/rss.xml", "source":"BBC"},
            {"rssFeedUrl":"https://news.google.com/rss/search?q=topstories&hl=en-US&gl=US&ceid=US:en", "source":"Google News"},
            {"rssFeedUrl":"https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=100003114", "source":"CNBC"}
        ],
        
        "Recent Stories":[
            {"rssFeedUrl":"https://frontline.thehindu.com/current-issue/feeder/default.rss", "source":"The Hindu"},
            {"rssFeedUrl":"https://feeds.feedburner.com/ndtvnews-latest", "source":"NDTV"},
            {"rssFeedUrl":"https://economictimes.indiatimes.com/rssfeedsdefault.cms", "source":"Economic Times"},
            {"rssFeedUrl":"https://economictimes.indiatimes.com/news/rssfeeds/1715249553.cms", "source":"Economic Times"},
            {"rssFeedUrl":"https://globalnews.ca/feed/", "source":"Global News"},
        ],

        "Technology": [
            {"rssFeedUrl":"https://frontline.thehindu.com/science-and-technology/feeder/default.rss", "source":"The Hindu"},
            {"rssFeedUrl":"https://feeds.feedburner.com/gadgets360-latest", "source":"NDTV"},
            {"rssFeedUrl":"https://timesofindia.indiatimes.com/rssfeeds/66949542.cms", "source":"Times of India"},  
            {"rssFeedUrl":"https://www.livemint.com/rss/technology", "source":"Mint"},
            {"rssFeedUrl":"https://economictimes.indiatimes.com/prime/technology-and-startups/rssfeeds/63319172.cms", "source":"Economic Times"},

            {"rssFeedUrl":"http://rss.cnn.com/rss/money_technology.rss", "source":"CNN"},
            {"rssFeedUrl":"https://feeds.bbci.co.uk/news/technology/rss.xml", "source":"BBC"},
            {"rssFeedUrl":"https://rss.nytimes.com/services/xml/rss/nyt/Technology.xml", "source":"The New York Times"},
            {"rssFeedUrl":"https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=19854910", "source":"CNBC"},
        ],
        "Sports": [
            {"rssFeedUrl":"https://sportstar.thehindu.com/feeder/default.rss", "source":"The Hindu"},
            {"rssFeedUrl":"https://feeds.feedburner.com/ndtvsports-latest", "source":"NDTV"},
            {"rssFeedUrl":"https://www.espncricinfo.com/ci/content/rss/feeds_rss_cricket.html", "source":"ESPN"},
            {"rssFeedUrl":"https://economictimes.indiatimes.com/news/sports/rssfeeds/26407562.cms", "source":"Economic Times"},
            {"rssFeedUrl":"https://www.livemint.com/rss/sports", "source":"Mint"},
            {"rssFeedUrl":"https://timesofindia.indiatimes.com/rssfeeds/4719148.cms", "source":"Times of India"},

            {"rssFeedUrl":"https://rss.nytimes.com/services/xml/rss/nyt/Sports.xml", "source":"The New York Times"},
            {"rssFeedUrl":"https://globalnews.ca/sports/feed/", "source":"Global News"},
            {"rssFeedUrl":"https://api.foxsports.com/v2/content/optimized-rss?partnerKey=MB0Wehpmuj2lUhuRhQaafhBjAJqaPU244mlTDK1i&aggregateId=7f83e8ca-6701-5ea0-96ee-072636b67336", "source":"Fox Sports"},
        ],

        "Business": [
            {"rssFeedUrl":"https://frontline.thehindu.com/economy/feeder/default.rss", "source":"The Hindu"},
            {"rssFeedUrl":"https://feeds.feedburner.com/ndtvprofit-latest", "source":"NDTV"},
            {"rssFeedUrl":"https://timesofindia.indiatimes.com/rssfeeds/1898055.cms", "source":"Times of India"},
            {"rssFeedUrl":"https://www.livemint.com/rss/money", "source":"Mint"},
            {"rssFeedUrl":"https://economictimes.indiatimes.com/small-biz/rssfeeds/5575607.cms", "source":"Economic Times"},

            {"rssFeedUrl":"http://rss.cnn.com/rss/money_smbusiness.rss", "source":"CNN"},
            {"rssFeedUrl":"https://rss.nytimes.com/services/xml/rss/nyt/Business.xml", "source":"The New York Times"},
            {"rssFeedUrl":"https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=10001147", "source":"CNBC"},
            {"rssFeedUrl":"https://globalnews.ca/money/feed/", "source":"Global News"},
        ],
        "Entertainment": [
            {"rssFeedUrl":"https://frontline.thehindu.com/arts-and-culture/feeder/default.rss", "source":"The Hindu"},
            {"rssFeedUrl":"https://feeds.feedburner.com/ndtvmovies-latest", "source":"NDTV"},
            {"rssFeedUrl":"https://timesofindia.indiatimes.com/rssfeeds/1081479906.cms", "source":"Times of India"},
            {"rssFeedUrl":"https://economictimes.indiatimes.com/industry/media/entertainment/rssfeeds/13357212.cms", "source":"Economic Times"},

            {"rssFeedUrl":"https://rss.nytimes.com/services/xml/rss/nyt/Movies.xml", "source":"The New York Times"},
            {"rssFeedUrl":"https://globalnews.ca/entertainment/feed/", "source":"Global News"},
            {"rssFeedUrl":"https://feeds.bbci.co.uk/news/entertainment_and_arts/rss.xml", "source":"BBC"},
        ],
        "Health":[
            {"rssFeedUrl":"https://frontline.thehindu.com/the-nation/public-health/feeder/default.rss", "source":"The Hindu"},
            {"rssFeedUrl":"https://feeds.feedburner.com/ndtvcooks-latest", "source":"NDTV"},
            {"rssFeedUrl":"https://timesofindia.indiatimes.com/rssfeeds/2886704.cms", "source":"Times of India"},
            {"rssFeedUrl":"https://economictimes.indiatimes.com/industry/healthcare/biotech/rssfeeds/13358050.cms", "source":"Economic Times"},
            

            {"rssFeedUrl":"https://rss.nytimes.com/services/xml/rss/nyt/Health.xml", "source":"The New York Times"},
            {"rssFeedUrl":"https://globalnews.ca/health/feed/", "source":"Global News"},
            {"rssFeedUrl":"https://news.un.org/feed/subscribe/en/news/topic/health/feed/rss.xml", "source":"United Nations"},
            {"rssFeedUrl":"https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=10000108", "source":"CNBC"},
            {"rssFeedUrl":"https://feeds.bbci.co.uk/news/health/rss.xml", "source":"BBC"},
        ],

        "Science":[
            {"rssFeedUrl":"https://frontline.thehindu.com/science-and-technology/feeder/default.rss", "source":"The Hindu"},
            {"rssFeedUrl":"https://timesofindia.indiatimes.com/rssfeeds/-2128672765.cms", "source":"Times of India"},
            {"rssFeedUrl":"https://livemint.com/rss/science", "source":"Mint"},
            {"rssFeedUrl":"https://economictimes.indiatimes.com/news/science/rssfeeds/39872847.cms", "source":"Economic Times"},
            
            {"rssFeedUrl":"https://rss.nytimes.com/services/xml/rss/nyt/Science.xml", "source":"The New York Times"},
            {"rssFeedUrl":"https://feeds.bbci.co.uk/news/science_and_environment/rss.xml", "source":"BBC"},
            
        ],
        
        "Finance":[
            {"rssFeedUrl":"https://frontline.thehindu.com/economy/feeder/default.rss", "source":"The Hindu"},
            {"rssFeedUrl":"https://www.livemint.com/rss/budget", "source":"Mint"},
            {"rssFeedUrl":"https://economictimes.indiatimes.com/industry/banking/finance/rssfeeds/13358259.cms", "source":"Economic Times"}
            ,
            {"rssFeedUrl":"http://rss.cnn.com/rss/money_pf.rss", "source":"CNN"},
            {"rssFeedUrl":"https://rss.nytimes.com/services/xml/rss/nyt/YourMoney.xml", "source":"The New York Times"},
            {"rssFeedUrl":"https://globalnews.ca/money/feed/", "source":"Global News"},
            {"rssFeedUrl":"https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=10000115", "source":"CNBC"},
        ],

        "Politics":[
            {"rssFeedUrl":"https://frontline.thehindu.com/politics/feeder/default.rss", "source":"The Hindu"},
            {"rssFeedUrl":"https://www.livemint.com/rss/elections", "source":"Mint"},
            {"rssFeedUrl":"https://economictimes.indiatimes.com/news/politics-and-nation/rssfeeds/1052732854.cms", "source":"Economic Times"},

            {"rssFeedUrl":"https://rss.nytimes.com/services/xml/rss/nyt/Politics.xml", "source":"The New York Times"},
            {"rssFeedUrl":"https://globalnews.ca/politics/feed/", "source":"Global News"},
            {"rssFeedUrl":"https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=10000113", "source":"CNBC"},
            {"rssFeedUrl":"https://feeds.bbci.co.uk/news/politics/rss.xml", "source":"BBC"},
        ],
        
        "Travel":[
            {"rssFeedUrl":"https://frontline.thehindu.com/other/travel/feeder/default.rss", "source":"The Hindu"},
            
            {"rssFeedUrl":"http://rss.cnn.com/rss/money_lifestyle.rss", "source":"CNN"},
            {"rssFeedUrl":"https://rss.nytimes.com/services/xml/rss/nyt/Travel.xml", "source":"The New York Times"},
            {"rssFeedUrl":"https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=10000739", "source":"CNBC"},
        ],

        "Education":[
            {"rssFeedUrl":"https://timesofindia.indiatimes.com/rssfeeds/913168846.cms", "source":"Times of India"},
            {"rssFeedUrl":"https://www.livemint.com/rss/education", "source":"Mint"},
            
            {"rssFeedUrl":"https://economictimes.indiatimes.com/nri/study/rssfeeds/79038794.cms", "source":"Economic Times"},
            {"rssFeedUrl":"https://rss.nytimes.com/services/xml/rss/nyt/Education.xml", "source":"The New York Times"},
            {"rssFeedUrl":"https://feeds.bbci.co.uk/news/education/rss.xml", "source":"BBC"},
        ]
    }

    scrape_all_feeds(feed_urls)
