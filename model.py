# scripts/model.py

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import joblib
import os

def train_model(df):
    """
    Train a regression model to predict future GDP levels as a proxy for crisis risk.
    This is an extremely simplified approach.
    """
    df = df.dropna().copy()
    # Features: SPY close pct change, lagged GDP, etc.
    features = ["GDP_lag1", "SPY_close_pct_change"]
    target = "GDPC1"

    X = df[features]
    y = df[target]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    print("Train score:", model.score(X_train, y_train))
    print("Test score:", model.score(X_test, y_test))

    return model

def predict_crisis(model, input_data):
    """
    Predict future GDP or crisis proxy using the trained model.
    input_data: DataFrame containing the same features used in training.
    """
    prediction = model.predict(input_data)
    return prediction

if __name__ == "__main__":
    # Example usage
    processed_df = pd.read_csv("data/processed/processed_data.csv", index_col=0)
    model = train_model(processed_df)

    # Save model
    model_dir = os.path.join("data", "models")
    os.makedirs(model_dir, exist_ok=True)
    joblib.dump(model, os.path.join(model_dir, "random_forest_model.pkl"))
