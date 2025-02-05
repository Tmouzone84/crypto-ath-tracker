import requests

url = "https://api.coingecko.com/api/v3/coins/markets"
params = {
    "vs_currency": "usd",  # Make sure this parameter is included
    "order": "market_cap_desc",
    "per_page": 10,
    "page": 1,
    "sparkline": "false"
}

response = requests.get(url, params=params)

# Print response to check if it works
print("Status Code:", response.status_code)
try:
    data = response.json()
    print("Response JSON:", data[:5])  # Print first 5 results
except Exception as e:
    print("Error decoding JSON:", e)
