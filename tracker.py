import streamlit as st
import pandas as pd
import requests

# Set Streamlit Page Title
st.set_page_config(page_title="Crypto ATH Breakout Tracker", layout="wide")

# Title & Description
st.title("🚀 Crypto ATH Breakout Tracker")
st.write("Live tracker for coins that have broken their previous all-time high.")

# Function to format large numbers
def format_large_number(num):
    if num >= 1_000_000_000:
        return f"{num / 1_000_000_000:.2f}B"
    elif num >= 1_000_000:
        return f"{num / 1_000_000:.2f}M"
    elif num >= 1_000:
        return f"{num / 1_000:.2f}K"
    return str(num)

# Function to fetch data from multiple pages
def fetch_coins(pages=5, per_page=100):  # Fetch 5 pages of 100 coins each (500 total)
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

# Fetch Data
coins_data = fetch_coins(pages=5, per_page=100)  # Fetch 500 coins

if coins_data:
    # Convert API data to DataFrame
    df = pd.DataFrame(coins_data)

    # Remove unnecessary columns
    df.drop(columns=["image"], inplace=True)

    # Format numerical columns for better readability
    df["current_price"] = df["current_price"].apply(format_large_number)
    df["market_cap"] = df["market_cap"].apply(format_large_number)
    df["fully_diluted_valuation"] = df["fully_diluted_valuation"].apply(lambda x: format_large_number(x) if pd.notna(x) else "N/A")

    # Rename columns for better readability
    df.rename(columns={
        "id": "ID",
        "symbol": "Symbol",
        "name": "Name",
        "current_price": "Current Price (USD)",
        "market_cap": "Market Cap",
        "market_cap_rank": "Market Cap Rank",
        "fully_diluted_valuation": "Fully Diluted Valuation",
        "ath": "ATH (USD)",
        "ath_date": "ATH Date"
    }, inplace=True)

    # Convert "Current Price" and "ATH" back to float for proper filtering
    df["Current Price (USD)"] = df["Current Price (USD)"].str.replace(",", "").astype(float)
    df["ATH (USD)"] = df["ATH (USD)"].str.replace(",", "").astype(float)

    # Filter coins breaking their ATH
    df["ATH Broken"] = df["Current Price (USD)"] > df["ATH (USD)"]
    df_ath = df[df["ATH Broken"] == True]

    # Display full dataset
    st.subheader("📊 All Coins Data")
    st.write("This table includes all coins fetched from CoinGecko.")
    st.dataframe(df[["Name", "Symbol", "Current Price (USD)", "ATH (USD)", "ATH Broken", "ATH Date"]])

    # Display filtered results separately
    st.subheader("🔥 Coins Breaking Their ATH")
    if not df_ath.empty:
        st.write("The table below only includes coins that have **broken their all-time high.**")
        st.dataframe(df_ath[["Name", "Symbol", "Current Price (USD)", "ATH (USD)", "ATH Date"]])
    else:
        st.write("🚨 No coins have broken their previous ATH yet!")

else:
    st.error("Failed to fetch data! No coins were retrieved.")
