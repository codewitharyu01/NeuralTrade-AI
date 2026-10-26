import pandas as pd
from features import add_features

# It is my Design....!!!
# ===============================
# Load Dataset
# ===============================

df = pd.read_csv("dataset/stock_dataset.csv")

df["Date"] = pd.to_datetime(df["Date"])

stocks = [
    "AAPL",
    "AMZN",
    "GOOGL",
    "META",
    "MSFT",
    "NVDA",
    "TSLA"
]

df = df[df["Ticker"].isin(stocks)]

print("Dataset Loaded")
print(df.shape)

# ===============================
# Create Features
# ===============================

all_data = []

for ticker in stocks:

    print(f"Processing {ticker}...")

    stock_df = df[df["Ticker"] == ticker].copy()

    stock_df = add_features(stock_df)

    # ----------------------------
    # Placeholder Sentiment
    # ----------------------------

    stock_df["Sentiment"] = 0

    # ----------------------------
    # Target (Next Day Close)
    # ----------------------------

    stock_df["Target"] = stock_df["Close"].shift(-1)

    all_data.append(stock_df)

# ===============================
# Merge all stocks
# ===============================

df = pd.concat(all_data)

# Remove missing values

df.dropna(inplace=True)

print("\nFinal Dataset Shape")
print(df.shape)

print("\nColumns")
print(df.columns)

print("\nSample Data")
print(df.head())

df.to_csv("dataset/final_dataset.csv", index=False)

print("Dataset saved Successfully")

# ===============================
# Train Machine Learning Model
# ===============================

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)
import joblib
import numpy as np

# Features

features = [
    "Open",
    "High",
    "Low",
    "Close",
    "Volume",
    "MA20",
    "MA50",
    "MA200",
    "RSI",
    "MACD",
    "MACD_SIGNAL",
    "MACD_DIFF",
    "BB_UPPER",
    "BB_LOWER",
    "Sentiment"
]

X = df[features]

y = df["Target"]

# Train Test Split

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

print("Training Samples :", len(X_train))
print("Testing Samples :", len(X_test))

# Model

model = RandomForestRegressor(
    n_estimators=200,
    max_depth=12,
    random_state=42,
    n_jobs=-1
)

print("\nTraining Model...")

model.fit(X_train, y_train)

print("Training Completed")

# ===============================
# Model Evaluation
# ===============================

predictions = model.predict(X_test)

mae = mean_absolute_error(y_test, predictions)

rmse = np.sqrt(mean_squared_error(y_test, predictions))

r2 = r2_score(y_test, predictions)

print("\n============== RESULTS ==============")

print("MAE :", round(mae,2))

print("RMSE :", round(rmse,2))

print("R2 Score :", round(r2,4))

# ===============================
# Save Model
# ===============================

joblib.dump(model, "models/stock_model.pkl")

print("\nModel Saved Successfully")

print("Location : models/stock_model.pkl")
importance = pd.DataFrame({
    "Feature": features,
    "Importance": model.feature_importances_
})

importance = importance.sort_values(
    by="Importance",
    ascending=False
)

print("\nTop Features")

print(importance)