from unittest.mock import patch
import pytest
from stock_market.services.stock_market import get_stock_data, InvalidSymbolError


@patch('stock_market.services.stock_market.requests')
def test_get_stock_data_successfully(mock_requests):
    mock_requests.get.return_value.json.return_value = {
        "Meta Data": {
            "1. Information": "Daily Prices (open, high, low, close) and Volumes",
            "2. Symbol": "AAPL",
            "3. Last Refreshed": "2022-07-25",
            "4. Output Size": "Compact",
            "5. Time Zone": "US/Eastern"
        },
        "Time Series (Daily)": {
            "2022-07-21": {
                "1. open": "128.7500",
                "2. high": "128.8100",
                "3. low": "125.1300",
                "4. close": "127.1500",
                "5. volume": "11975361"
            },
            "2022-07-25": {
                "1. open": "128.4400",
                "2. high": "129.1257",
                "3. low": "127.9000",
                "4. close": "128.5400",
                "5. volume": "4702352"
            },
            "2022-07-22": {
                "1. open": "127.0300",
                "2. high": "128.3200",
                "3. low": "125.7100",
                "4. close": "128.2500",
                "5. volume": "6467205"
            },
        }
    }

    result = get_stock_data("AAPL")

    assert result.open_price == "128.4400"
    assert result.higher_price == "129.1257"
    assert result.lower_price == "127.9000"
    assert result.close_price_variation == "0.23%"


@patch('stock_market.services.stock_market.requests')
def test_get_stock_data_failed_with_invalid_symbol(mock_requests):
    mock_requests.get.return_value.json.return_value = {
        'Error Message': 'Test message'
    }

    with pytest.raises(InvalidSymbolError):
        get_stock_data("invalid")
