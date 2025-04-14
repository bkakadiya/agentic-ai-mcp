import os
import pytest

from unittest.mock import patch
from services.corporate_actions import get_dividends, get_stock_splits
import requests

@pytest.fixture
def mock_env_key():
    with patch.dict(os.environ, {"ALPHA_VANTAGE_KEY": "TEST_KEY"}):
        yield

@patch('services.corporate_actions.requests.get')
def test_get_dividends_success(mock_get, mock_env_key):
    mock_response = mock_get.return_value
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = {"AAPL": [{"exDate": "2024-01-01", "paymentDate": "2024-01-15"}]}
    data = get_dividends('AAPL')
    assert data is not None
    assert "AAPL" in data
    assert len(data['AAPL']) == 1
    mock_get.assert_called_once()

@patch('services.corporate_actions.requests.get')
def test_get_dividends_failure(mock_get, mock_env_key):
    mock_response = mock_get.return_value
    mock_response.raise_for_status.side_effect = requests.exceptions.RequestException("API Error")
    data = get_dividends('AAPL')
    assert data is None
    mock_get.assert_called_once()

@patch('services.corporate_actions.requests.get')
def test_get_stock_splits_success(mock_get, mock_env_key):
    mock_response = mock_get.return_value
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = {"TSLA": [{"splitDate": "2022-08-25", "splitFactor": "3:1"}]}
    data = get_stock_splits('TSLA')
    assert data is not None
    assert "TSLA" in data
    assert len(data['TSLA']) == 1
    mock_get.assert_called_once()

@patch('services.corporate_actions.requests.get')
def test_get_stock_splits_failure(mock_get, mock_env_key):
    mock_response = mock_get.return_value
    mock_response.raise_for_status.side_effect = requests.exceptions.RequestException("API Error")
    data = get_stock_splits('TSLA')
    assert data is None
    mock_get.assert_called_once()