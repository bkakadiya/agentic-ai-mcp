import os
import requests

ALPHA_VANTAGE_KEY = os.environ.get("ALPHA_VANTAGE_KEY")
BASE_URL = "https://www.alphavantage.co/query?"

if not ALPHA_VANTAGE_KEY:
    raise EnvironmentError(
        "Please set the ALPHA_VANTAGE_KEY environment variable."
    )

def get_news_sentiment(tickers=None, topics=None, time_from=None, time_to=None, sort='latest'):
    """Fetches news sentiment data."""
    params = {
        'function': 'NEWS_SENTIMENT',
        'sort': sort,
        'apikey': ALPHA_VANTAGE_KEY
    }
    if tickers:
        params['tickers'] = tickers
    if topics:
        params['topics'] = topics
    if time_from:
        params['time_from'] = time_from
    if time_to:
        params['time_to'] = time_to
    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching news sentiment: {e}")
        return None

if __name__ == '__main__':
    print("Example: Fetching news sentiment for Apple")
    aapl_news = get_news_sentiment(tickers='AAPL')
    if aapl_news and 'feed' in aapl_news:
        print(aapl_news['feed'][:1])