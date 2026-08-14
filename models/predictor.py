import joblib
import pandas as pd

model = joblib.load("models/stock_model.pkl")


def predict_price(
        open_price,
        high,
        low,
        close,
        volume,
        ma20,
        ma50,
        ma200,
        rsi,
        macd,
        macd_signal,
        macd_diff,
        bb_upper,
        bb_lower,
        sentiment
):

    data = pd.DataFrame([{

        "Open": open_price,
        "High": high,
        "Low": low,
        "Close": close,
        "Volume": volume,

        "MA20": ma20,
        "MA50": ma50,
        "MA200": ma200,

        "RSI": rsi,

        "MACD": macd,
        "MACD_SIGNAL": macd_signal,
        "MACD_DIFF": macd_diff,

        "BB_UPPER": bb_upper,
        "BB_LOWER": bb_lower,

        "Sentiment": sentiment

    }])

    prediction = model.predict(data)[0]

    return round(prediction, 2)