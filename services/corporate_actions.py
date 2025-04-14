import os
import requests

ALPHA_VANTAGE_KEY = os.environ.get("ALPHA_VANTAGE_KEY")
BASE_URL = "https://www.alphavantage.co/query?"

if not ALPHA_VANTAGE_KEY:
    raise EnvironmentError(
        "Please set the ALPHA_VANTAGE_KEY environment variable."
    )

def get_dividends(symbol):
    """Fetches dividend events for a given symbol."""
    params = {
        'function': 'DIVIDENDS',
        'symbol': symbol,
        'apikey': ALPHA_VANTAGE_KEY
    }
    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching dividends: {e}")
        return None

def get_stock_splits(symbol):
    """Fetches stock split events for a given symbol."""
    params = {
        'function': 'SPLITS',
        'symbol': symbol,
        'apikey': ALPHA_VANTAGE_KEY
    }
    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching stock splits: {e}")
        return None

if __name__ == '__main__':
    print("Example: Fetching Apple dividends")
    aapl_dividends = get_dividends('AAPL')
    if aapl_dividends:
        #Print key value pair in a separate lines
        for date, dividend in aapl_dividends.items():
            print(f"{date}: {dividend}")

    print("\nExample: Fetching Tesla stock splits")
    tsla_splits = get_stock_splits('TSLA')
    if tsla_splits:
        #Print splits in new lines
        for date, split in tsla_splits.items():
            print(f"{date}: {split}")