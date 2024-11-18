# database/crud.py
import sqlite3
from datetime import datetime,timedelta

DB_PATH = 'news_db.sqlite3'

def create_connection():
    """Create and return a database connection."""
    conn = sqlite3.connect(DB_PATH)
    return conn

def create_tables():
    """Create the necessary tables in the database."""
    conn = create_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS rss_feeds (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        description TEXT,
        link TEXT,
        published_date TEXT,
        source TEXT,
        UNIQUE(title, published_date)
    )
    ''')
    conn.commit()
    conn.close()

def insert_rss_feed(title, description, link, published_date, source):
    """Insert an RSS feed entry into the database."""
    conn = create_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
    INSERT INTO rss_feeds (title, description, link, published_date, source)
    VALUES (?, ?, ?, ?, ?)
    ''', (title, description, link, published_date, source))
    
    conn.commit()
    conn.close()

def fetch_news(source, start_date, end_date):
    """Fetch news based on source and date range."""
    conn = create_connection()
    cursor = conn.cursor()

    # Format the start date with the time set to 00:00:00
    start_date_str = start_date.strftime('%Y-%m-%d 00:00:00')

    # Format the end date with the time set to 23:59:59
    end_date = end_date + timedelta(days=1) - timedelta(seconds=1)
    end_date_str = end_date.strftime('%Y-%m-%d 23:59:59')

    query = '''
    SELECT title, description, link, published_date, source
    FROM rss_feeds
    WHERE source = ?
    AND published_date BETWEEN ? AND ?
    ORDER BY published_date DESC
    '''
    
    cursor.execute(query, (source, start_date_str, end_date_str))
    rows = cursor.fetchall()
    
    conn.close()
    return rows


def check_duplicate(title, published_date):
    conn = create_connection()
    cursor = conn.cursor()

    query = '''
    SELECT 1 FROM rss_feeds WHERE title = ? AND published_date = ?
    '''
    
    cursor.execute(query, (title, published_date))
    result = cursor.fetchone()
    
    conn.close()
    
    return result is not None  # True if duplicate exists
