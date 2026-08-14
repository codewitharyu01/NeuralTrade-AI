from flask import Flask, render_template, request, session
from utils.data_fetcher import get_stock_data, get_historical_data
from utils.indicators import calculate_indicators
from utils.news import get_news
from utils.sentiment import analyze_sentiment
from models.predictor import predict_price
from datetime import datetime
from database import init_db, register_user, login_user

app = Flask(__name__)
app.secret_key = "neuraltrade-secret-key"
init_db()

@app.route("/register", methods=["POST"])
def register():
    fullname = request.form["fullname"]
    email = request.form["email"]
    password = request.form["password"]

    if register_user(fullname,email,password):
        return {"status":"success"}
    else:
        return {"status":"exists"}

@app.route("/login", methods=["POST"])    
def login():
    email = request.form["email"].strip().lower()
    password = request.form["password"]

    user = login_user(email,password)
    if user:
        session["user"] = {
            "fullname" : user["fullname"],
            "email" : user["email"]
        }
        return {"status" : "success",
                "user" : session["user"]
                }
    return {"status" : "failed",
            "message" : "Incorrect email or password."
            }

@app.route("/logout", methods=["POST"])
def logout():
    session.pop("user", None)
    return {"status":"success"}
    
@app.route("/",methods=["GET", "POST"])
def home():
    user = session.get("user")
    stock = None

    if request.method == "POST":
        symbol = request.form["symbol"].upper()
        period = request.form["period"]
    else:
        symbol = "AAPL"    
        period = "1mo"

    stock = get_stock_data(symbol)   

    if not stock or stock.get("current_price") is None:

        error = f"'{symbol}' is not a valid stock symbol. Please enter a valid stock ticker (e.g. AAPL, TSLA, MSFT, NVDA, AMZN).Showing AAPL instead."

        symbol = "AAPL"
        period = "1mo"

        stock = get_stock_data(symbol)

    else:

       error = None

    watchlist_symbols = [
    "AAPL",
    "MSFT",
    "NVDA",
    "TSLA",
    "AMZN",
    "GOOGL"
]

    watchlist = []

    for sym in watchlist_symbols:

        try:

            data = get_stock_data(sym)

            # 1 Year History
            hist = get_historical_data(sym, "1y")
            hist = calculate_indicators(hist)

            latest = hist.iloc[-1]

            ma20 = round(latest["MA20"], 2)
            ma50 = round(latest["MA50"], 2)
            ma200 = round(latest["MA200"], 2)

            rsi = round(latest["RSI"], 2)

            macd = round(latest["MACD"], 2)
            macd_signal = round(latest["MACD_SIGNAL"], 2)
            macd_diff = round(latest["MACD_DIFF"], 2)

            bb_upper = round(latest["BB_Upper"], 2)
            bb_lower = round(latest["BB_Lower"], 2)

            # News
            news_data = get_news(sym)
            news_data = analyze_sentiment(news_data)

            sentiment_score = (
                round(
                    sum(x["score"] for x in news_data) / len(news_data),
                    2
                )
                if news_data else 0
            )

            # AI Prediction
            predicted = predict_price(
    
                data["open"],
                data["high"],
                data["low"],
                data["current_price"],
                data["volume"],

                ma20,
                ma50,
                ma200,

                rsi,

                macd,
                macd_signal,
                macd_diff,

                bb_upper,
                bb_lower,

                sentiment_score
            )

            expected_change = round(
                ((predicted - data["close"]) / data["close"]) * 100,
                2
            ) 

            # ===========================
            # AI Recommendation Engine
            # ===========================

            score = 0

            # 1. Prediction (40 Marks)
            if expected_change >= 1:
                score += 40
            elif expected_change <= -1:
                score -= 40

            # 2. RSI (15 Marks)
            if rsi < 30:
                score += 15
            elif rsi > 70:
                score -= 15

            # 3. MACD (15 Marks)
            if macd > 0:
                score += 15
            else:
                score -= 15

            # 4. Moving Average (10 Marks)
            if data["current_price"] > ma20:
                score += 5
            else:
                score -= 5
    
            if data["current_price"] > ma50:
                score += 5
            else:
                score -= 5

            # 5. News Sentiment (20 Marks)
            if sentiment_score > 0.10:
                score += 20
            elif sentiment_score < -0.10:
                score -= 20

            # Final Recommendation
            if score >= 40:
                recommendation = "BUY"
                trend = "Uptrend"

            elif score <= -40:
                recommendation = "SELL"
                trend = "Downtrend"

            else:
                recommendation = "HOLD"
                trend = "Sideways"

            confidence = min(
                95,
                max(
                    60,
                    round(70 + abs(score)*0.4)
                )
            )

            watchlist.append({

            "company": data["company"],

            "symbol": sym,

            "price": round(data["current_price"], 2),

            "change": expected_change,

            "prediction": predicted,

            "recommendation": recommendation,

            "trend": trend,

            "confidence": confidence,

            "score": score

        })

        except Exception as e:

            print(f"Watchlist Error ({sym}) :", e)

    history = get_historical_data(symbol, period)

    dates = history.index.astype(str).tolist()
    prices = history["Close"].tolist()

    indicator_history = get_historical_data(symbol, "1y")

    
    indicator_history = calculate_indicators(indicator_history)
    latest = indicator_history.iloc[-1]

    ma20 = round(latest["MA20"],2)
    ma50 = round(latest["MA50"],2)
    ma200 = round(latest["MA200"],2)
    rsi = round(latest["RSI"],2)
    macd = round(latest["MACD"],2)
    macd_signal = round(latest["MACD_SIGNAL"], 2)
    macd_diff = round(latest["MACD_DIFF"], 2)

    bb_upper = round(latest["BB_Upper"],2)
    bb_lower = round(latest["BB_Lower"],2)

    if rsi < 30:
        rsi_status = "Bullish"
    elif rsi > 70:
        rsi_status = "Bearish"
    else:
        rsi_status = "Neutral"

    macd_status = "Bullish" if macd > 0 else "Bearish"
    ma20_status = "Bullish" if stock["current_price"] > ma20 else "Bearish"
    ma50_status = "Bullish" if stock["current_price"] > ma50 else "Bearish"
    ma200_status = "Bullish" if stock["current_price"] > ma200 else "Bearish"

    if stock["current_price"] > bb_upper:
        bb_status = "Bearish"
    elif stock["current_price"] < bb_lower:
        bb_status = "Bullish"
    else:
        bb_status = "Neutral"

    # -------------------------------
    # News Fetching
    # -------------------------------

    news = get_news(symbol)

    news = analyze_sentiment(news)



    positive = sum(1 for item in news if item["sentiment"] == "Positive")

    negative = sum(1 for item in news if item["sentiment"] == "Negative")

    neutral = sum(1 for item in news if item["sentiment"] == "Neutral")


    average_score = round(

        sum(item["score"] for item in news) / len(news),

    2

    ) if news else 0 

        
                
    sentiment_score = 0 if not news else average_score  

    predicted_price = predict_price(

        stock["open"],
        stock["high"],
        stock["low"],
        stock["current_price"],
        stock["volume"],
    
        ma20,
        ma50,
        ma200,
    
        rsi,
    
        macd,
        macd_signal,
        macd_diff,
    
        bb_upper,
        bb_lower,
    
        sentiment_score
    
    ) 

    expected_change = round(

        ((predicted_price - stock["close"])
        / stock["current_price"]) * 100,

        2

    )

    # ===========================
    # AI Recommendation Engine
    # ===========================

    score = 0

    # 1. Prediction (40 Marks)
    if expected_change >= 1:
        score += 40
    elif expected_change <= -1:
        score -= 40

    # 2. RSI (15 Marks)
    if rsi < 30:
        score += 15
    elif rsi > 70:
        score -= 15

    # 3. MACD (15 Marks)
    if macd > 0:
        score += 15
    else:
        score -= 15

    # 4. Moving Average (10 Marks)
    if stock["current_price"] > ma20:
        score += 5
    else:
        score -= 5

    if stock["current_price"] > ma50:
        score += 5
    else:
        score -= 5

    # 5. News Sentiment (20 Marks)
    if average_score > 0.10:
        score += 20
    elif average_score < -0.10:
        score -= 20

    if score >= 40:
        recommendation = "BUY" 
    elif score <= -40:
        recommendation = "SELL"
    else:
        recommendation = "HOLD"   
    
    if score >= 40:
        trend = "Uptrend" 
    elif score <= -40:
        trend = "Downtrend"
    else:
        trend = "Sideways"

    confidence = min(95, 
                     max(60, 
                             round(70 + abs(score) * 0.4)))

    """confidence = max(
        60,
        min(
            95,
            round(95 - abs(expected_change),1)
        )
    )"""

    """if expected_change >= 1:

        if average_score > 0.10:
            recommendation = "BUY"

        elif average_score < -0.10:
            recommendation = "HOLD"

        else:
            recommendation = "HOLD"

    elif expected_change <= -1:

        if average_score < -0.10:
            recommendation = "SELL"

        else:
            recommendation = "HOLD"

    else:
        recommendation = "HOLD"

        

    if expected_change >= 1 and confidence >= 80:
        trend = "Uptrend"

    elif expected_change < -1 and confidence >= 80:
        trend = "Downtrend"

    else: 
        trend = "Sideways" 
        """    
        
      

    # ===========================
    # AI Insights
    # ===========================

    # Trend Strength
    if score >= 60:
        trend_strength = "Very Strong"

    elif score >= 40:
        trend_strength = "Strong"
    
    elif score >= 15:
        trend_strength = "Moderate"
    
    elif score <= -60:
        trend_strength = "Very Strong Bearish"

    elif score <= -40:
        trend_strength = "Strong Bearish"
    
    elif score <= -15:
        trend_strength = "Moderate Bearish"

    else:
        trend_strength = "Sideways"


    # Risk Level
    if confidence >= 90 and abs(expected_change) < 2:
        risk_level = "Low"

    elif confidence >= 75:
        risk_level = "Moderate"

    else:
        risk_level = "High"


    # Feature Importance
    if abs(average_score) > 0.20:
        feature_importance = "News Sentiment"

    elif rsi < 30 or rsi > 70:
        feature_importance = "RSI"

    elif abs(macd) > abs(macd_signal):
        feature_importance = "MACD"

    else:
        feature_importance = "Moving Average"


    # Volatility
    volatility = f"{abs(expected_change):.2f}%"


    # AI Insights
    insights = [

        {
            "label": "Prediction Confidence",
            "value": f"{confidence}%"
        },
    
        {
            "label": "Risk Level",
            "value": risk_level
        },
    
        {
            "label": "Trend Strength",
            "value": trend_strength
        },
    
        {
            "label": "Feature Importance",
            "value": feature_importance
        },
    
        {
            "label": "Volatility",
            "value": volatility
        },
    
        {
            "label": "Model Used",
            "value": "Random Forest + Technical + Sentiment"
        }
    
    ]

    target_horizon = "Next Trading day"

    recent_predictions = []

    recent_predictions.insert(0,{
        "company":stock["company"],
        "current_price":stock["current_price"],
        "predicted_price":predicted_price,
        "recommendation":recommendation,
        "confidence":confidence,
        "date":datetime.now().strftime("%d-%m-%Y %H:%M")
    })
    recent_predictions[:] = recent_predictions[:5]

    return render_template(
        "dashboard.html",
        user = user,
        stock = stock,
        symbol = symbol,
        period = period,
        prices = prices,
        dates = dates,
        ma20 = ma20,
        ma50 = ma50,
        ma200 = ma200,
        rsi = rsi,
        macd = macd,
        bb_upper = bb_upper,
        bb_lower = bb_lower,
        rsi_status = rsi_status,
        macd_status = macd_status,
        ma200_status = ma200_status,
        ma50_status = ma50_status,
        bb_status = bb_status,
        ma20_status = ma20_status,
        news = news,
        positive = positive,
        neutral = neutral,
        negative = negative,
        average_score = average_score,
        predicted_price = predicted_price,
        expected_change = expected_change,
        recommendation = recommendation,
        confidence = confidence,
        target_horizon = target_horizon,
        trend = trend,
        score = score,
        watchlist = watchlist,
        insights = insights,
        recent_predictions=recent_predictions,
        error = error
        )

if __name__ == "__main__":
    # Debug mode for development
    app.run(debug=True)