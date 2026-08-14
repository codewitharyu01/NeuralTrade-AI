# Make the Technical Indicators in dataset.

import ta

def add_features(df):

    df = df.sort_values("Date")

    df["MA20"] = ta.trend.sma_indicator(df["Close"], window=20)
    df["MA50"] = ta.trend.sma_indicator(df["Close"], window=50)
    df["MA200"] = ta.trend.sma_indicator(df["Close"], window=200)

    df["RSI"] = ta.momentum.RSIIndicator(df["Close"]).rsi()

    macd = ta.trend.MACD(df["Close"])

    df["MACD"] = macd.macd()
    df["MACD_SIGNAL"] = macd.macd_signal()
    df["MACD_DIFF"] = macd.macd_diff()

    bb = ta.volatility.BollingerBands(df["Close"])

    df["BB_UPPER"] = bb.bollinger_hband()
    df["BB_LOWER"] = bb.bollinger_lband()

    return df