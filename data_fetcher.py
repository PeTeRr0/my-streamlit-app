# scripts/data_fetcher.py

import requests
import pandas as pd
import datetime
import os
from config import FRED_API_KEY, STOCK_API_KEY  # Example - store your keys in config.py

FRED_BASE_URL = "https://api.stlouisfed.org/fred/series/observations"
STOCK_API_URL = "https://www.alphavantage.co/query"

def fetch_fred_data(series_id="GDPC1", start_date="2000-01-01", end_date="2024-12-31"):
    """
    Fetch data for a given FRED series (e.g., real GDP) from start_date to end_date.
    """
    params = {
        "series_id": series_id,
        "api_key": FRED_API_KEY,
        "file_type": "json",
        "observation_start": start_date,
        "observation_end": end_date
    }
    response = requests.get(FRED_BASE_URL, params=params)
    data = response.json()["observations"]

    # Convert to DataFrame
    df = pd.DataFrame(data)
    df["value"] = pd.to_numeric(df["value"], errors="coerce")
    df["date"] = pd.to_datetime(df["date"])
    return df[["date", "value"]].rename(columns={"value": series_id})

def fetch_stock_data(symbol="SPY", function="TIME_SERIES_DAILY", output_size="compact"):
    """
    Fetch daily stock data (e.g., S&P 500 ETF = SPY) from Alpha Vantage or similar.
    """
    params = {
        "function": function,
        "symbol": symbol,
        "apikey": STOCK_API_KEY,
        "outputsize": output_size
    }
    response = requests.get(STOCK_API_URL, params=params)
    data = response.json().get("Time Series (Daily)", {})
    
    # Convert nested JSON to DataFrame
    df = pd.DataFrame.from_dict(data, orient='index')
    df.index = pd.to_datetime(df.index)
    df = df.rename(columns={
        "1. open": "Open",
        "2. high": "High",
        "3. low": "Low",
        "4. close": "Close",
        "5. volume": "Volume"
    })
    df.sort_index(inplace=True)
    return df

if __name__ == "__main__":
    # Example usage:
    fred_df = fetch_fred_data()
    stock_df = fetch_stock_data()

    # Save to data/raw
    raw_dir = os.path.join("data", "raw")
    os.makedirs(raw_dir, exist_ok=True)
    fred_df.to_csv(os.path.join(raw_dir, "fred_data.csv"), index=False)
    stock_df.to_csv(os.path.join(raw_dir, "stock_data.csv"))
