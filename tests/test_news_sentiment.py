import os
import pytest
import requests
from unittest.mock import patch
from services.news_sentiment import get_news_sentiment

@pytest.fixture
def mock_env_key():
    with patch.dict(os.environ, {"ALPHA_VANTAGE_KEY": "TEST_KEY"}):
        yield

@patch('services.news_sentiment.requests.get')
def test_get_news_sentiment_success(mock_get, mock_env_key):
    mock_response = mock_get.return_value
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = {"feed": [{"title": "News 1"}, {"title": "News 2"}]}
    data = get_news_sentiment(tickers='AAPL')
    assert data is not None
    assert "feed" in data
    assert len(data['feed']) == 2
    mock_get.assert_called_once()

@patch('services.news_sentiment.requests.get')
def test_get_news_sentiment_failure(mock_get, mock_env_key):
    mock_response = mock_get.return_value
    mock_response.raise_for_status.side_effect = requests.exceptions.RequestException("API Error")
    data = get_news_sentiment(tickers='AAPL')
    assert data is None
    mock_get.assert_called_once()

@patch('services.news_sentiment.requests.get')
def test_get_news_sentiment_with_params(mock_get, mock_env_key):
    mock_response = mock_get.return_value
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = {"feed": []}
    get_news_sentiment(tickers='GOOGL', topics='technology', time_from='20230101')
    mock_get.assert_called_once()
    args, kwargs = mock_get.call_args
    assert 'tickers' in kwargs['params']
    assert 'topics' in kwargs['params']
    assert 'time_from' in kwargs['params']