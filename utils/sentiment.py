from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()

def analyze_sentiment(news):

    analyzed_news = []

    for item in news:

        score = analyzer.polarity_scores(item["title"])["compound"]

        if score >= 0.05:
            sentiment = "Positive"

        elif score <= -0.05:
            sentiment = "Negative"

        else:
            sentiment = "Neutral"

        item["score"] = round(score, 2)

        item["sentiment"] = sentiment

        analyzed_news.append(item)

    return analyzed_news
