import os
import pytest
import requests
from unittest.mock import patch
from services.earnings import get_earnings

@pytest.fixture
def mock_env_key():
    with patch.dict(os.environ, {"ALPHA_VANTAGE_KEY": "TEST_KEY"}):
        yield

@patch('services.earnings.requests.get')
def test_get_earnings_success(mock_get, mock_env_key):
    mock_response = mock_get.return_value
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = {"annualReports": [], "quarterlyReports": []}
    data = get_earnings('MSFT')
    assert data is not None
    assert "annualReports" in data
    assert "quarterlyReports" in data
    mock_get.assert_called_once()

@patch('services.earnings.requests.get')
def test_get_earnings_failure(mock_get, mock_env_key):
    mock_response = mock_get.return_value
    mock_response.raise_for_status.side_effect = requests.exceptions.RequestException("API Error")
    data = get_earnings('MSFT')
    assert data is None
    mock_get.assert_called_once()

@patch('services.earnings.requests.get')
def test_get_earnings_empty_reports(mock_get, mock_env_key):
    mock_response = mock_get.return_value
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = {}
    data = get_earnings('GOOGL')
    assert data is not None
    assert not data
    mock_get.assert_called_once()