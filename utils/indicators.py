from ta.trend import SMAIndicator, MACD
from ta.momentum import RSIIndicator
from ta.volatility import BollingerBands

def calculate_indicators(history):

    # ===============================
    # Moving Averages
    # ===============================

    history["MA20"] = SMAIndicator(
        close=history["Close"],
        window=20
    ).sma_indicator()
    
    history["MA50"] = SMAIndicator(
        close=history["Close"],
        window=50
    ).sma_indicator()

    history["MA200"] = SMAIndicator(
        close=history["Close"],
        window=200
    ).sma_indicator()

    # ===============================
    # RSI
    # ===============================

    history["RSI"] = RSIIndicator(
        close=history["Close"],
        window=14
    ).rsi()

    # ===============================
    # MACD
    # ===============================

    macd = MACD(close=history["Close"])

    history["MACD"] = macd.macd()

    history["MACD_SIGNAL"] = macd.macd_signal()

    history["MACD_DIFF"] = macd.macd_diff()

    # ===============================
    # Bollinger bands
    # ===============================

    bb = BollingerBands(
        close=history["Close"],
        window=20
    )
    
    history["BB_Upper"] = bb.bollinger_hband()
    history["BB_Lower"] = bb.bollinger_lband()
    
    return history