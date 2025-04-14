import os
import requests

ALPHA_VANTAGE_KEY = os.environ.get("ALPHA_VANTAGE_KEY")
BASE_URL = "https://www.alphavantage.co/query?"

if not ALPHA_VANTAGE_KEY:
    raise EnvironmentError(
        "Please set the ALPHA_VANTAGE_KEY environment variable."
    )

def get_company_overview(symbol):
    """Fetches the company overview data."""
    params = {
        'function': 'OVERVIEW',
        'symbol': symbol,
        'apikey': ALPHA_VANTAGE_KEY
    }
    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching company overview: {e}")
        return None

def get_etf_profile(symbol):
    """Fetches the ETF profile data."""
    params = {
        'function': 'ETF_PROFILE',
        'symbol': symbol,
        'apikey': ALPHA_VANTAGE_KEY
    }
    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching ETF profile: {e}")
        return None

if __name__ == '__main__':
    print("Example: Fetching IBM company overview")
    ibm_overview = get_company_overview('IBM')
    if ibm_overview:
        print(list(ibm_overview.keys())[:2])

    print("\nExample: Fetching SPY ETF profile")
    spy_profile = get_etf_profile('SPY')
    if spy_profile:
        print(list(spy_profile.keys())[:2])