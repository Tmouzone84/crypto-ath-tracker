import streamlit as st
import pandas as pd
import requests
import time

# Streamlit UI Config
st.set_page_config(page_title="Crypto ATH Tracker", layout="wide")
st.title(" Mouzone ATH Breakout Tracker")
st.write("Live tracker for coins that have broken their previous all-time high.")

# ✅ Use the free CoinGecko API (No API key required)
API_BASE_URL = "https://api.coingecko.com/api/v3/coins/markets"

# Function to fetch crypto data
def fetch_coins(pages=5, per_page=100):
    all_coins = []
    for page in range(1, pages + 1):
        params = {
            "vs_currency": "usd",
            "order": "market_cap_desc",
            "per_page": per_page,
            "page": page,
            "sparkline": False
        }

        response = requests.get(API_BASE_URL, params=params)

        if response.status_code == 200:
            coins_data = response.json()
            if not coins_data:
                break
            all_coins.extend(coins_data)
        elif response.status_code == 429:
            st.error("⏳ **Rate Limited!** Retrying after 60 seconds...")
            time.sleep(60)
            continue
        else:
            st.error(f"Failed to fetch page {page}: Status Code {response.status_code}")
            break

        time.sleep(1.5)  # Small delay to avoid rate limits

    return all_coins

# Fetch Data
coins_data = fetch_coins(pages=10, per_page=100)

if coins_data:
    df = pd.DataFrame(coins_data)
    df["ATH Broken"] = df["current_price"] > df["ath"]
    df_ath_usd = df[df["ATH Broken"]]

    st.subheader("🔥 Coins that Broke ATH in USD")
    st.dataframe(df_ath_usd[["name", "symbol", "current_price", "ath", "market_cap", "last_updated"]])
else:
    st.error("🚨 No coins were retrieved! Check CoinGecko free API rate limits.")

