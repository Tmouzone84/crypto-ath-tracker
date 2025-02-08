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
    # Convert API data to DataFrame
    df = pd.DataFrame(coins_data)

    # Ensure columns are cleaned for human-readable format
    df["current_price"] = pd.to_numeric(
        df["current_price"].astype(str).str.replace(",", "", regex=True),
        errors="coerce"
    )
    df["ath"] = pd.to_numeric(
        df["ath"].astype(str).str.replace(",", "", regex=True),
        errors="coerce"
    )

    # Filter coins that have broken their previous ATH
    df["ATH Broken"] = df["current_price"] > df["ath"]

    # Separate into two tables: All coins and Coins breaking ATH in USD
    df_ath_usd = df[df["ATH Broken"] == True]

    # Display all coins data
    st.subheader("📊 Coins Data (Before Filtering)")
    st.dataframe(df[["id", "symbol", "name", "current_price", "ath"]])

    # Show coins breaking ATH
    st.subheader("🔥 Coins that Broke ATH in USD")
    if not df_ath_usd.empty:
        st.dataframe(df_ath_usd[["id", "symbol", "name", "current_price", "ath"]])
    else:
        st.write("🚨 No coins have broken their previous ATH yet!")

else:
    st.error("Failed to fetch data! No coins were retrieved.")
