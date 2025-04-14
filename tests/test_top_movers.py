import os
import pytest
import requests
from unittest.mock import patch
from services.top_movers import get_top_gainers_losers

@pytest.fixture
def mock_env_key():
    with patch.dict(os.environ, {"ALPHA_VANTAGE_KEY": "TEST_KEY"}):
        yield

@patch('services.top_movers.requests.get')
def test_get_top_gainers_losers_success(mock_get, mock_env_key):
    mock_response = mock_get.return_value
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = {"top_gainers": [{"ticker": "ABC"}], "top_losers": [{"ticker": "XYZ"}]}
    data = get_top_gainers_losers()
    assert data is not None
    assert "top_gainers" in data
    assert "top_losers" in data
    assert len(data['top_gainers']) == 1
    assert len(data['top_losers']) == 1
    mock_get.assert_called_once()

@patch('services.top_movers.requests.get')
def test_get_top_gainers_losers_failure(mock_get, mock_env_key):
    mock_response = mock_get.return_value
    mock_response.raise_for_status.side_effect = requests.exceptions.RequestException("API Error")
    data = get_top_gainers_losers()
    assert data is None
    mock_get.assert_called_once()

@patch('services.top_movers.requests.get')
def test_get_top_gainers_losers_empty(mock_get, mock_env_key):
    mock_response = mock_get.return_value
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = {}
    data = get_top_gainers_losers()
    assert data is not None
    assert not data  # Check if the dictionary is empty
    mock_get.assert_called_once()