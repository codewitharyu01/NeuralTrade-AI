import yfinance as yf

ticker = yf.Ticker("AAPL")

df = ticker.history(period="1mo")

print(df.head())
print("Empty:", df.empty)