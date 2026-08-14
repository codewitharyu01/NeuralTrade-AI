import feedparser

def get_news(symbol):

    url = f"https://news.google.com/rss/search?q={symbol}+stock"

    feed = feedparser.parse(url)

    news = []

    for entry in feed.entries[:10]:

        news.append({

            "title": entry.title,

            "source": getattr(entry, "source", {}).get("title", "Google News"),

            "date": entry.published,

            "link": entry.link

        })

    return news
