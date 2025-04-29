from datetime import datetime
from unittest.mock import Mock, patch

import pytest

from src.services.mb_candle_service import MercadoBitcoinService


@pytest.fixture
def sample_api_response():
    return {"c": ["500.00", "1000.00"], "t": [1652119200, 1652187600]}


@patch("src.services.mb_candle_service.requests.get")
def test_fetch_candles_success(mock_get, sample_api_response):
    mock_response = Mock()
    mock_response.json.return_value = sample_api_response
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    symbol = "BTC-BRL"
    from_ts = 1652119200
    to_ts = 1652187600

    candles = MercadoBitcoinService.fetch_candles(symbol, from_ts, to_ts)

    assert len(candles) == 2
    assert candles[0]["timestamp"] == datetime.fromtimestamp(1652119200)
    assert candles[0]["close"] == 500.0
    assert candles[1]["timestamp"] == datetime.fromtimestamp(1652187600)
    assert candles[1]["close"] == 1000.0
