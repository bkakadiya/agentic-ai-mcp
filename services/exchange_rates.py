import os
import requests

ALPHA_VANTAGE_KEY = os.environ.get("ALPHA_VANTAGE_KEY")
BASE_URL = "https://www.alphavantage.co/query?"

if not ALPHA_VANTAGE_KEY:
    raise EnvironmentError(
        "Please set the ALPHA_VANTAGE_KEY environment variable."
    )

def get_exchange_rate(from_currency, to_currency):
    """Fetches the real-time exchange rate for a currency pair."""
    params = {
        'function': 'CURRENCY_EXCHANGE_RATE',
        'from_currency': from_currency,
        'to_currency': to_currency,
        'apikey': ALPHA_VANTAGE_KEY
    }
    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching exchange rate: {e}")
        return None

def get_currency_time_series(from_currency, to_currency, interval='daily', outputsize='compact'):
    """Fetches daily, weekly, or monthly time series data for a currency pair."""
    function = f"FX_{interval.upper()}"
    params = {
        'function': function,
        'from_symbol': from_currency,
        'to_symbol': to_currency,
        'outputsize': outputsize,
        'apikey': ALPHA_VANTAGE_KEY
    }
    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching currency time series: {e}")
        return None

def get_digital_currency_exchange_rate(symbol, market):
    """Fetches the real-time exchange rate for a digital currency pair."""
    params = {
        'function': 'DIGITAL_CURRENCY_EXCHANGE_RATE',
        'symbol': symbol,
        'market': market,
        'apikey': ALPHA_VANTAGE_KEY
    }
    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching digital currency exchange rate: {e}")
        return None

def get_digital_currency_time_series(symbol, market, interval='daily', outputsize='compact'):
    """Fetches daily, weekly, or monthly time series data for a digital currency pair."""
    function = f"DIGITAL_CURRENCY_{interval.upper()}"
    params = {
        'function': function,
        'symbol': symbol,
        'market': market,
        'outputsize': outputsize,
        'apikey': ALPHA_VANTAGE_KEY
    }
    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching digital currency time series: {e}")
        return None

if __name__ == '__main__':
    print("Example: Fetching USD to EUR exchange rate")
    usd_eur = get_exchange_rate('USD', 'EUR')
    if usd_eur and 'Realtime Currency Exchange Rate' in usd_eur:
        print(usd_eur['Realtime Currency Exchange Rate']['5. Exchange Rate'])

    print("\nExample: Fetching BTC to USD exchange rate")
    btc_usd = get_digital_currency_exchange_rate('BTC', 'USD')
    if btc_usd and 'Realtime Currency Exchange Rate' in btc_usd:
        print(btc_usd['Realtime Currency Exchange Rate']['5. Exchange Rate'])