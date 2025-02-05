import streamlit as st
import pandas as pd
import requests

# Set Streamlit Page Title
st.set_page_config(page_title="Crypto ATH Breakout Tracker", layout="wide")

# Title & Description
st.title("🚀 Crypto ATH Breakout Tracker")
st.write("Live tracker for coins that have broken their previous all-time high.")

# Function to fetch multiple pages of data (up to 500 coins)
def fetch_coins(pages=5, per_page=100):
    url = "https://api.coingecko.com/api/v3/coins/markets"
    all_coins = []

    for page in range(1, pages + 1):
        params = {
            "vs_currency": "usd",
            "order": "market_cap_desc",
            "per_page": per_page,
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

# Function to format large numbers (e.g., 1000000 -> 1M)
def format_number(num):
    if pd.isna(num) or num is None:
        return "-"
    num = float(num)
    if num >= 1_000_000_000:
        return f"{num / 1_000_000_000:.2f}B"
    elif num >= 1_000_000:
        return f"{num / 1_000_000:.2f}M"
    elif num >= 1_000:
        return f"{num / 1_000:.2f}K"
    else:
        return f"{num:.2f}"

# Fetch Data
coins_data = fetch_coins(pages=5, per_page=100)

if coins_data:
    # Convert API data to DataFrame
    df = pd.DataFrame(coins_data)

    # 🔍 Fix Filtering Issue: Ensure ATH is compared correctly
    df["ATH Broken"] = df.apply(lambda row: row["current_price"] > row["ath"] if pd.notna(row["ath"]) else False, axis=1)

    # Filter coins breaking ATH in USD
    df_ath_usd = df[df["ATH Broken"] == True]

    # Format Numbers for Readability
    df_ath_usd["Current Price (USD)"] = df_ath_usd["current_price"].apply(format_number)
    df_ath_usd["ATH (USD)"] = df_ath_usd["ath"].apply(format_number)
    df_ath_usd["Market Cap"] = df_ath_usd["market_cap"].apply(format_number)
    df_ath_usd["24h Volume"] = df_ath_usd["total_volume"].apply(format_number)

    # Select & Rename Columns for Better Readability
    df_display = df_ath_usd[["name", "symbol", "Current Price (USD)", "ATH (USD)", "Market Cap", "24h Volume", "ATH Broken", "last_updated"]]
    df_display = df_display.rename(columns={
        "name": "Name",
        "symbol": "Symbol",
        "last_updated": "Last Updated"
    })

    # Show Debugging Info
    st.subheader("📌 Debugging Info")
    st.write(f"Total Coins Fetched: {len(df)}")
    st.write(f"Coins Breaking ATH in USD: {len(df_ath_usd)}")

    # Show results
    st.subheader("🔥 Coins that Broke ATH in USD")
    if not df_display.empty:
        st.dataframe(df_display)
    else:
        st.write("🚨 No coins have broken their previous ATH yet!")

else:
    st.error("Failed to fetch data! No coins were retrieved.")
