import streamlit as st
import pandas as pd
import requests
import time

# Set Streamlit Page Title
st.set_page_config(page_title="Crypto ATH Breakout Tracker", layout="wide")

# Title & Description
st.title("Crypto ATH Breakout Tracker")
st.write("Live tracker for coins that have broken their previous all-time high.")

# Function to format large numbers into human-readable format
def format_number(value):
    if pd.isna(value):
        return "N/A"
    elif value >= 1_000_000_000:
        return f"{value / 1_000_000_000:.2f}B"
    elif value >= 1_000_000:
        return f"{value / 1_000_000:.2f}M"
    elif value >= 1_000:
        return f"{value / 1_000:.2f}K"
    else:
        return f"{value:.2f}"

# Function to fetch data with retries
def fetch_coins(pages=5, per_page=100):  # Fetch up to 500 coins
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

        retries = 3  # Number of retries
        for attempt in range(retries):
            response = requests.get(url, params=params)
            if response.status_code == 200:
                coins_data = response.json()
                if not coins_data:
                    break  # Stop if no more data
                all_coins.extend(coins_data)
                break
            elif response.status_code == 429:
                st.warning("⏳ Rate Limited! Retrying in 60 seconds...")
                time.sleep(60)  # Wait 60 seconds before retrying
            else:
                st.error(f"Failed to fetch page {page}: Status Code {response.status_code}")
                return []
    
    return all_coins

# Fetch Data
coins_data = fetch_coins(pages=5, per_page=100)  # Fetch 500 coins

if coins_data:
    # Convert API data to DataFrame
    df = pd.DataFrame(coins_data)

    # Format numbers for better readability
    df["Market Cap"] = df["market_cap"].apply(format_number)
    df["Current Price (USD)"] = df["current_price"].apply(format_number)
    df["All-Time High (USD)"] = df["ath"].apply(format_number)
    df["ATH Broken"] = df["current_price"] > df["ath"]
    df["Last Updated"] = pd.to_datetime(df["last_updated"]).dt.strftime('%Y-%m-%d %H:%M:%S')

    # Select only useful columns
    df_cleaned = df[["name", "symbol", "Current Price (USD)", "All-Time High (USD)", "Market Cap", "ATH Broken", "Last Updated"]]

    # Filter for coins breaking ATH
    df_ath_usd = df_cleaned[df_cleaned["ATH Broken"] == True]

    # Display Summary
    st.subheader("Summary")
    st.write(f"Total Coins Fetched: **{len(df)}**")
    st.write(f"Coins Breaking ATH in USD: **{len(df_ath_usd)}**")

    # Show all coins before filtering
    st.subheader("📊 All Fetched Coins Data (Before Filtering)")
    st.dataframe(df_cleaned)

    # Show filtered coins breaking ATH
    st.subheader("Coins that Broke ATH in USD")
    if not df_ath_usd.empty:
        st.dataframe(df_ath_usd)
    else:
        st.write("No coins have broken their previous ATH yet!")

else:
    st.error("Failed to fetch data! No coins were retrieved.")
