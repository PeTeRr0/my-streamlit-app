# streamlit_app.py

import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os
from datetime import datetime, timedelta

from data_fetcher import fetch_fred_data, fetch_stock_data
from data_preprocessor import merge_datasets, preprocess_data
from model import predict_crisis


MODEL_PATH = os.path.join("data", "models", "random_forest_model.pkl")

def load_model():
    if os.path.exists(MODEL_PATH):
        model = joblib.load(MODEL_PATH)
        return model
    else:
        st.error("No trained model found. Please train your model first.")
        return None

def main():
    st.title("Real-Time Economic Crisis Predictor")

    # Sidebar for user inputs
    st.sidebar.subheader("Data Fetch Settings")
    series_id = st.sidebar.text_input("FRED Series ID", value="GDPC1")
    stock_symbol = st.sidebar.text_input("Stock Symbol", value="SPY")

    if st.sidebar.button("Fetch & Predict"):
        st.write("Fetching real-time data...")

        # Fetch data
        fred_df = fetch_fred_data(series_id=series_id)
        stock_df = fetch_stock_data(symbol=stock_symbol)

        # Merge and preprocess
        merged_df = merge_datasets(fred_df, stock_df)
        processed_df = preprocess_data(merged_df)

        # Load model
        model = load_model()
        if model is not None:
            # Take the latest row as an example for "current state" input
            latest_input = processed_df.iloc[[-1]][["GDP_lag1", "SPY_close_pct_change"]]
            pred = predict_crisis(model, latest_input)
            st.success(f"Predicted GDP: {pred[0]:.2f}")

            # Placeholder for crisis threshold logic
            # If predicted GDP < some threshold => crisis risk
            threshold = 18000  # Example threshold
            if pred[0] < threshold:
                st.error("High risk of economic crisis.")
            else:
                st.info("No immediate crisis risk indicated.")

        st.write("Real-time data fetch complete.")
    
    st.markdown("___")
    st.write("This is a demo application that shows how to fetch data, preprocess it, and predict crisis risk in real-time. Customize the model and data sources to fit your use case.")

if __name__ == "__main__":
    main()
