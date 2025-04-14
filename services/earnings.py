import os
import requests

ALPHA_VANTAGE_KEY = os.environ.get("ALPHA_VANTAGE_KEY")
BASE_URL = "https://www.alphavantage.co/query?"

if not ALPHA_VANTAGE_KEY:
    raise EnvironmentError(
        "Please set the ALPHA_VANTAGE_KEY environment variable."
    )

def get_earnings(symbol):
    """Fetches annual and quarterly earnings for a given symbol."""
    params = {
        'function': 'EARNINGS',
        'symbol': symbol,
        'apikey': ALPHA_VANTAGE_KEY
    }
    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching earnings: {e}")
        return None

if __name__ == '__main__':
    print("Example: Fetching Microsoft earnings")
    msft_earnings = get_earnings('MSFT')
    if msft_earnings:
        print(list(msft_earnings.keys())[:2])