import streamlit as st
import pandas as pd
import requests

# Set Streamlit Page Title
st.set_page_config(page_title="Crypto ATH Breakout Tracker", layout="wide")

# Title & Description
st.title("🚀 Crypto ATH Breakout Tracker")
st.write("Live tracker for coins that have broken their previous all-time high.")

# Function to fetch data from multiple pages
def fetch_coins(pages=5, per_page=100):  # Fetch 5 pages of 100 coins each (500 total)
    url = "https://api.coingecko.com/api/v3/coins/markets"
    all_coins = []

    for page in range(1, pages + 1):
        params = {
            "vs_currency": "usd",
            "order": "market_cap_desc",
            "per_page": per_page,  # Max per page is 250
            "page": page,
            "sparkline": False
        }
        response = requests.get(url, params=params)

        if response.status_code == 200:
            coins_data = response.json()
            if not coins_data:
                break  # Stop if no more data
            all_coins.extend(coins_data)
        else:
            st.error(f"Failed to fetch page {page}: Status Code {response.status_code}")
            break

    return all_coins

# Fetch Data
coins_data = fetch_coins(pages=5, per_page=100)  # Fetch 500 coins

if coins_data:
    # Debug: Show full API response in Streamlit
    st.subheader("🔍 Raw API Data (Before Filtering)")
    st.write(coins_data)

    # Convert API data to DataFrame
    df = pd.DataFrame(coins_data)

    # Debug: Display raw DataFrame in Streamlit
    st.subheader("📊 All Fetched Coins Data (Before Filtering)")
    st.dataframe(df)

    # Filter coins that have broken their previous ATH
    df["ATH Broken"] = df["current_price"] > df["ath"]

    # Separate
