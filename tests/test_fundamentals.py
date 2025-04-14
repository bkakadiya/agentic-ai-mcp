import os
import pytest
import requests
from unittest.mock import patch
from services.fundamentals import get_company_overview, get_etf_profile

@pytest.fixture
def mock_env_key():
    with patch.dict(os.environ, {"ALPHA_VANTAGE_KEY": "TEST_KEY"}):
        yield

@patch('services.fundamentals.requests.get')
def test_get_company_overview_success(mock_get, mock_env_key):
    mock_response = mock_get.return_value
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = {"Symbol": "AAPL", "AssetType": "Common Stock"}
    data = get_company_overview('AAPL')
    assert data is not None
    assert "Symbol" in data
    assert data['Symbol'] == "AAPL"
    mock_get.assert_called_once()

@patch('services.fundamentals.requests.get')
def test_get_company_overview_failure(mock_get, mock_env_key):
    mock_response = mock_get.return_value
    mock_response.raise_for_status.side_effect = requests.exceptions.RequestException("API Error")
    data = get_company_overview('AAPL')
    assert data is None
    mock_get.assert_called_once()

@patch('services.fundamentals.requests.get')
def test_get_etf_profile_success(mock_get, mock_env_key):
    mock_response = mock_get.return_value
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = {"Symbol": "SPY", "Name": "SPDR S&P 500 ETF Trust"}
    data = get_etf_profile('SPY')
    assert data is not None
    assert "Symbol" in data
    assert data['Name'] == "SPDR S&P 500 ETF Trust"
    mock_get.assert_called_once()

@patch('services.fundamentals.requests.get')
def test_get_etf_profile_failure(mock_get, mock_env_key):
    mock_response = mock_get.return_value
    mock_response.raise_for_status.side_effect = requests.exceptions.RequestException("API Error")
    data = get_etf_profile('SPY')
    assert data is None
    mock_get.assert_called_once()