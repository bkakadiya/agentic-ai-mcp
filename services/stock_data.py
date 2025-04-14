import os
import requests

ALPHA_VANTAGE_KEY = os.environ.get("ALPHA_VANTAGE_KEY")
BASE_URL = "https://www.alphavantage.co/query?"

if not ALPHA_VANTAGE_KEY:
    raise EnvironmentError(
        "Please set the ALPHA_VANTAGE_KEY environment variable."
    )

def get_time_series(symbol, interval='daily', adjusted=False, outputsize='compact'):
    """Fetches daily, weekly, or monthly time series data for a given symbol."""
    function = f"TIME_SERIES_{interval.upper()}"
    if adjusted and interval.lower() == 'daily':
        function = "TIME_SERIES_DAILY_ADJUSTED"
    params = {
        'function': function,
        'symbol': symbol,
        'outputsize': outputsize,
        'apikey': ALPHA_VANTAGE_KEY
    }
    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching time series data: {e}")
        return None

def search_ticker(keywords):
    """Searches for tickers based on keywords."""
    params = {
        'function': 'SYMBOL_SEARCH',
        'keywords': keywords,
        'apikey': ALPHA_VANTAGE_KEY
    }
    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error searching ticker: {e}")
        return None

if __name__ == '__main__':
    print("Example: Fetching Apple daily data")
    aapl_daily = get_time_series('AAPL')
    if aapl_daily:
        print(list(aapl_daily.keys())[:2])

    print("\nExample: Searching for Tesla")
    tesla_search = search_ticker('Tesla')
    if tesla_search and 'bestMatches' in tesla_search:
        print(tesla_search['bestMatches'][:2])