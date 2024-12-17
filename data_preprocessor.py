# scripts/data_preprocessor.py

import pandas as pd
import numpy as np
import os

def merge_datasets(fred_df, stock_df):
    """
    Merge macroeconomic data (FRED) with stock market data on a time axis.
    """
    # Resample stock data to monthly or unify the frequency to match GDP frequency
    stock_monthly = stock_df.resample("M").last()  # Last day in each month for example

    # We'll also rename the date columns in fred_df to index
    fred_df.set_index("date", inplace=True)
    
    # Merge on date index
    merged_df = fred_df.join(stock_monthly["Close"], how="inner")
    return merged_df

def preprocess_data(df):
    """
    Clean and transform the merged dataset for modeling.
    Example transformations: filling missing values, generating lags, etc.
    """
    df = df.copy()
    # Fill missing values
    df.fillna(method="ffill", inplace=True)
    df.dropna(inplace=True)

    # Generate lags or additional features
    df["GDP_lag1"] = df["GDPC1"].shift(1)
    df["SPY_close_pct_change"] = df["Close"].pct_change()
    
    df.dropna(inplace=True)
    return df

if __name__ == "__main__":
    # Example usage after fetching
    raw_dir = os.path.join("data", "raw")
    fred_df = pd.read_csv(os.path.join(raw_dir, "fred_data.csv"))
    stock_df = pd.read_csv(os.path.join(raw_dir, "stock_data.csv"), parse_dates=True, index_col=0)

    merged = merge_datasets(fred_df, stock_df)
    processed = preprocess_data(merged)

    processed_dir = os.path.join("data", "processed")
    os.makedirs(processed_dir, exist_ok=True)
    processed.to_csv(os.path.join(processed_dir, "processed_data.csv"))
