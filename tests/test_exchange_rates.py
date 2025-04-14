import os
import pytest
import requests
from unittest.mock import patch
from services.exchange_rates import (
    get_exchange_rate,
    get_currency_time_series,
    get_digital_currency_exchange_rate,
    get_digital_currency_time_series
)


@pytest.fixture
def mock_env_key():
    with patch.dict(os.environ, {"ALPHA_VANTAGE_KEY": "TEST_KEY"}):
        yield

@patch('services.exchange_rates.requests.get')
def test_get_exchange_rate_success(mock_get, mock_env_key):
    mock_response = mock_get.return_value
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = {"Realtime Currency Exchange Rate": {"5. Exchange Rate": "1.10"}}
    data = get_exchange_rate('USD', 'EUR')
    assert data is not None
    assert "Realtime Currency Exchange Rate" in data
    assert "5. Exchange Rate" in data["Realtime Currency Exchange Rate"]
    mock_get.assert_called_once()

@patch('services.exchange_rates.requests.get')
def test_get_exchange_rate_failure(mock_get, mock_env_key):
    mock_response = mock_get.return_value
    mock_response.raise_for_status.side_effect = requests.exceptions.RequestException("API Error")
    data = get_exchange_rate('USD', 'EUR')
    assert data is None
    mock_get.assert_called_once()

@patch('services.exchange_rates.requests.get')
def test_get_currency_time_series_success(mock_get, mock_env_key):
    mock_response = mock_get.return_value
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = {"Meta Data": {}, "Time Series FX (Daily)": {"2025-04-11": {"1. open": "1.08"}}}
    data = get_currency_time_series('EUR', 'USD')
    assert data is not None
    assert "Meta Data" in data
    assert "Time Series FX (Daily)" in data
    assert "2025-04-11" in data["Time Series FX (Daily)"]
    mock_get.assert_called_once()

@patch('services.exchange_rates.requests.get')
def test_get_currency_time_series_failure(mock_get, mock_env_key):
    mock_response = mock_get.return_value
    mock_response.raise_for_status.side_effect = requests.exceptions.RequestException("API Error")
    data = get_currency_time_series('EUR', 'USD')
    assert data is None
    mock_get.assert_called_once()

@patch('services.exchange_rates.requests.get')
def test_get_digital_currency_exchange_rate_success(mock_get, mock_env_key):
    mock_response = mock_get.return_value
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = {"Realtime Currency Exchange Rate": {"5. Exchange Rate": "30000.00"}}
    data = get_digital_currency_exchange_rate('BTC', 'USD')
    assert data is not None
    assert "Realtime Currency Exchange Rate" in data
    assert "5. Exchange Rate" in data["Realtime Currency Exchange Rate"]
    mock_get.assert_called_once()

@patch('services.exchange_rates.requests.get')
def test_get_digital_currency_exchange_rate_failure(mock_get, mock_env_key):
    mock_response = mock_get.return_value
    mock_response.raise_for_status.side_effect = requests.exceptions.RequestException("API Error")
    data = get_digital_currency_exchange_rate('BTC', 'USD')
    assert data is None
    mock_get.assert_called_once()

@patch('services.exchange_rates.requests.get')
def test_get_digital_currency_time_series_success(mock_get, mock_env_key):
    mock_response = mock_get.return_value
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = {"Meta Data": {}, "Time Series (Digital Currency Daily)": {"2025-04-11": {"1a. open (USD)": "29500.00"}}}
    data = get_digital_currency_time_series('BTC', 'USD')
    assert data is not None
    assert "Meta Data" in data
    assert "Time Series (Digital Currency Daily)" in data
    assert "2025-04-11" in data["Time Series (Digital Currency Daily)"]
    mock_get.assert_called_once()

@patch('services.exchange_rates.requests.get')
def test_get_digital_currency_time_series_failure(mock_get, mock_env_key):
    mock_response = mock_get.return_value
    mock_response.raise_for_status.side_effect = requests.exceptions.RequestException("API Error")
    data = get_digital_currency_time_series('BTC', 'USD')
    assert data is None
    mock_get.assert_called_once()

@patch('services.exchange_rates.requests.get')
def test_get_exchange_rate_empty_response(mock_get, mock_env_key):
    mock_response = mock_get.return_value
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = {}
    data = get_exchange_rate('GBP', 'JPY')
    assert data is not None
    assert not data
    mock_get.assert_called_once()

@patch('services.exchange_rates.requests.get')
def test_get_currency_time_series_no_data(mock_get, mock_env_key):
    mock_response = mock_get.return_value
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = {"Meta Data": {}, "Time Series FX (Daily)": {}}
    data = get_currency_time_series('CAD', 'AUD', interval='daily')
    assert data is not None
    assert "Meta Data" in data
    assert "Time Series FX (Daily)" in data
    assert not data["Time Series FX (Daily)"]
    mock_get.assert_called_once()

@patch('services.exchange_rates.requests.get')
def test_get_digital_currency_exchange_rate_invalid_market(mock_get, mock_env_key):
    mock_response = mock_get.return_value
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = {}
    data = get_digital_currency_exchange_rate('ETH', 'INVALID')
    assert data is not None
    assert not data
    mock_get.assert_called_once()

@patch('services.exchange_rates.requests.get')
def test_get_digital_currency_time_series_weekly(mock_get, mock_env_key):
    mock_response = mock_get.return_value
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = {"Meta Data": {}, "Time Series (Digital Currency Weekly)": {"2025-04-07": {"1a. open (USD)": "28000.00"}}}
    data = get_digital_currency_time_series('BTC', 'USD', interval='weekly')
    assert data is not None
    assert "Meta Data" in data
    assert "Time Series (Digital Currency Weekly)" in data
    assert "2025-04-07" in data["Time Series (Digital Currency Weekly)"]
    mock_get.assert_called_once()