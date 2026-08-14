import yfinance as yf

def get_stock_data(symbol):

    stock = yf.Ticker(symbol)

    info = stock.info

    data = {
        "company": info.get("longName"),
        "symbol": info.get("symbol"),
        "open": info.get("open"),
        "high": info.get("dayHigh"),
        "low": info.get("dayLow"),
        "close": info.get("previousClose"),
        "volume": info.get("volume"),
        "market_cap": info.get("marketCap"),
        "current_price": info.get("currentPrice")
    }

    return data

def get_historical_data(symbol,period):
    
    stock = yf.Ticker(symbol)
    history = stock.history(period=period)

    return history