import streamlit as st
import pandas as pd
import requests

# Set Streamlit Page Title
st.set_page_config(page_title="Crypto ATH Breakout Tracker", layout="wide")

# Title & Description
st.title("🚀 Crypto ATH Breakout Tracker")
st.write("Live tracker for coins that have broken their previous all-time high.")

# Fetch data from CoinGecko API
url = "https://api.coingecko.com/api/v3/coins/markets"
params = {
    "vs_currency": "usd",
    "order": "market_cap_desc",
    "per_page": 50,  # Get more data to increase chances of ATH breakouts
    "page": 1,
    "sparkline": False
}

response = requests.get(url, params=params)

if response.status_code == 200:
    coins_data = response.json()

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

    # Separate into two tables: Coins breaking ATH in USD and BTC
    df_ath_usd = df[df["ATH Broken"] == True]

    # Display Debugging Info
    st.subheader("📌 Debugging Info")
    st.write(f"Total Coins Fetched: {len(df)}")
    st.write(f"Coins Breaking ATH in USD: {len(df_ath_usd)}")

    # Show results
    st.subheader("🔥 Coins that Broke ATH in USD")
    if not df_ath_usd.empty:
        st.dataframe(df_ath_usd[["name", "symbol", "current_price", "ath", "ATH Broken", "last_updated"]])
    else:
        st.write("🚨 No coins have broken their previous ATH yet!")

else:
    st.error(f"Failed to fetch data! API Status Code: {response.status_code}")

