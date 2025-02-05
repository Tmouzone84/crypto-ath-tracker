import requests
import pandas as pd
import streamlit as st
import datetime

# Fetch live crypto data
def fetch_crypto_data():
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": 100,
        "page": 1,
        "sparkline": "false"
    }

    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Error fetching data: {response.status_code}")
        return []

# Process data and check for ATH breakouts
def process_data(data):
    records = []
    for coin in data:
        name = coin["name"]
        symbol = coin["symbol"].upper()
        current_price = coin["current_price"]
        ath_price = coin["ath"]
        ath_broken = current_price >= ath_price

        records.append({
            "Name": name,
            "Symbol": symbol,
            "Current Price (USD)": current_price,
            "ATH (USD)": ath_price,
            "ATH Broken": "✅" if ath_broken else "❌",
            "Last Updated": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
    
    return pd.DataFrame(records)

# Fetch & Process Data
crypto_data = fetch_crypto_data()
df = process_data(crypto_data)

# Streamlit Dashboard
st.set_page_config(page_title="Crypto ATH Tracker", layout="wide")
st.title("🚀 Crypto ATH Breakout Tracker")
st.write("Live tracker for coins that have broken their previous all-time high.")

# Display results
st.subheader("Coins that Broke ATH in USD")
st.dataframe(df[df["ATH Broken"] == "✅"])

# Save history for tracking
df.to_csv("ath_history.csv", index=False, mode="a", header=False)

