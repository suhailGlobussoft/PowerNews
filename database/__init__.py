import sqlite3

# Connect to SQLite3 database (this will create the file if it doesn't exist)
conn = sqlite3.connect('news_db.sqlite3')

# Create a cursor object using the connection
cursor = conn.cursor()