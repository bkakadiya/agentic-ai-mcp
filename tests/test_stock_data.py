import os
import pytest
import requests
from unittest.mock import patch
from services.stock_data import get_time_series, search_ticker

@pytest.fixture
def mock_env_key():
    with patch.dict(os.environ, {"ALPHA_VANTAGE_KEY": "TEST_KEY"}):
        yield

@patch('services.stock_data.requests.get')
def test_get_time_series_success(mock_get, mock_env_key):
    mock_response = mock_get.return_value
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = {"Meta Data": {}, "Time Series (Daily)": {}}
    data = get_time_series('AAPL')
    assert data is not None
    assert "Meta Data" in data
    mock_get.assert_called_once()

@patch('services.stock_data.requests.get')
def test_get_time_series_failure(mock_get, mock_env_key):
    mock_response = mock_get.return_value
    mock_response.raise_for_status.side_effect = requests.exceptions.RequestException("API Error")
    data = get_time_series('AAPL')
    assert data is None
    mock_get.assert_called_once()

@patch('services.stock_data.requests.get')
def test_search_ticker_success(mock_get, mock_env_key):
    mock_response = mock_get.return_value
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = {"bestMatches": []}
    results = search_ticker('Tesla')
    assert results is not None
    assert "bestMatches" in results
    mock_get.assert_called_once()

@patch('services.stock_data.requests.get')
def test_search_ticker_failure(mock_get, mock_env_key):
    mock_response = mock_get.return_value
    mock_response.raise_for_status.side_effect = requests.exceptions.RequestException("API Error")
    results = search_ticker('Tesla')
    assert results is None
    mock_get.assert_called_once()