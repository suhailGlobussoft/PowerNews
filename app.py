from datetime import datetime
import streamlit as st
import json
import os
from datetime import datetime

# Directory where JSON files are stored
JSON_DIR = "rss_feeds_data"

# Load JSON data for a given category
@st.cache_data
def load_json_data(category):
    file_path = os.path.join(JSON_DIR, f"{category.lower()}.json")
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    return []

# Filter the data by source, date, and category
def filter_data(data, source=None, start_date=None, end_date=None):
    filtered_data = []

    for item in data:
        # Filter by source
        if source and item['source'] != source:
            continue

        # Filter by date range
        published_date_str = item.get('published', item.get('scraped_at'))
        try:
            published_date = datetime.fromisoformat(published_date_str)
        except ValueError:
            published_date = None

        # If published_date is timezone-aware, convert to naive (removing timezone info)
        if published_date and published_date.tzinfo is not None:
            published_date = published_date.replace(tzinfo=None)

        # Filter based on date range
        if start_date and published_date and published_date < start_date:
            continue
        if end_date and published_date and published_date > end_date:
            continue

        filtered_data.append(item)

    return filtered_data


# List of available categories (You can hard-code or fetch from available JSON files)
def get_available_categories():
    return [filename.split('.')[0].capitalize() for filename in os.listdir(JSON_DIR) if filename.endswith('.json')]

# Main Streamlit app function
def main():
    st.title("RSS Feed Viewer")

    # User input for Category
    categories = get_available_categories()
    category = st.selectbox("Select Category", categories)

    # Load the data for the selected category
    data = load_json_data(category)
    
    # Get unique sources from the data
    sources = sorted(set(item['source'] for item in data))
    
    # User input for Source filter
    source = st.selectbox("Select Source", ["All"] + sources)

    # User input for Date range filter
    start_date = st.date_input("Start Date", value=None)
    end_date = st.date_input("End Date", value=None)

    # Button to trigger the filtering
    if st.button("Show News"):
        # Convert date inputs to datetime objects
        start_date_dt = datetime.combine(start_date, datetime.min.time()) if start_date else None
        end_date_dt = datetime.combine(end_date, datetime.max.time()) if end_date else None

        # Filter the data based on user input
        filtered_data = filter_data(
            data, 
            source=None if source == "All" else source, 
            start_date=start_date_dt, 
            end_date=end_date_dt
        )

        # Display filtered data
        st.write(f"Showing {len(filtered_data)} results")
        for item in filtered_data:
            st.subheader(item['title'])
            st.write(f"Source: {item['source']}")
            st.write(f"Published: {item.get('published', 'N/A')}")
            st.write(f"[Read more]({item['link']})")

if __name__ == "__main__":
    main()
