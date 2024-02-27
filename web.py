import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_data(url, table_index):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for 4xx and 5xx status codes
        soup = BeautifulSoup(response.text, "html.parser")
        tables = soup.find_all("table")
        if tables:
            selected_table = tables[table_index]
            rows = selected_table.find_all("tr")
            data = []
            for row in rows:
                cells = row.find_all(["td", "th"])
                row_data = [cell.get_text(strip=True) for cell in cells]
                data.append(row_data)
            return data
        else:
            st.warning("No tables found on the webpage.")
            return None
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to fetch data from the provided URL: {e}")
        return None

def main():
    st.title("Web Scraping")
    url = st.text_input("Enter the URL of the webpage:")
    if url:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        tables = soup.find_all("table")
        if tables:
            table_options = [f"Table {i+1}" for i in range(len(tables))]
            table_index = st.selectbox("Select a table:", table_options)
            table_index = int(table_index.split()[1]) - 1  # Convert back to zero-based index
            if st.button("Scrape Data"):
                scraped_data = scrape_data(url, table_index)
                if scraped_data:
                    df = pd.DataFrame(scraped_data)
                    st.write("Scraped Data:")
                    st.write(df)
        else:
            st.warning("No tables found on the webpage.")

if __name__ == "__main__":
    main()
