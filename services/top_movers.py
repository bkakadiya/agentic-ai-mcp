import os
import requests

ALPHA_VANTAGE_KEY = os.environ.get("ALPHA_VANTAGE_KEY")
BASE_URL = "https://www.alphavantage.co/query?"

if not ALPHA_VANTAGE_KEY:
    raise EnvironmentError(
        "Please set the ALPHA_VANTAGE_KEY environment variable."
    )

def get_top_gainers_losers():
    """Fetches the top 5 gainers and losers."""
    params = {
        'function': 'TOP_GAINERS_LOSERS',
        'apikey': ALPHA_VANTAGE_KEY
    }
    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching top gainers/losers: {e}")
        return None

if __name__ == '__main__':
    print("Example: Fetching top gainers and losers")
    top_movers = get_top_gainers_losers()
    if top_movers:
        if 'top_gainers' in top_movers:
            print("Top Gainers:", top_movers['top_gainers'][:1])
        if 'top_losers' in top_movers:
            print("Top Losers:", top_movers['top_losers'][:1])