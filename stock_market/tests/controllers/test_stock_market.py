from unittest.mock import patch
from rest_framework.test import APIClient

from stock_market.controllers.utils import TokenAuthentication
from stock_market.models import User
from rest_framework.permissions import IsAuthenticated

from stock_market.services.stock_market import StockData, InvalidSymbolError
from rest_framework import exceptions


@patch.object(TokenAuthentication, 'authenticate_credentials')
@patch.object(IsAuthenticated, 'has_permission', return_value=True)
@patch('stock_market.controllers.stock_market.get_stock_data')
def test_stocks_api_call_successful(mock_get_stock_data, mock_permissions, mock_authentication):
    test_token = 'test_token'
    test_user = User(email='test@gmail.com', name='name', last_name='last_name')
    mock_authentication.return_value = (test_user, test_token)
    mock_get_stock_data.return_value = StockData("128.4400", "129.1257", "127.9000", "0.23%")

    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + test_token)
    response = client.get('/stocks/IMB')

    assert response.status_code == 200
    assert response.data == {
        'open_price': '128.4400',
        'higher_price': '129.1257',
        'lower_price': '127.9000',
        'close_price_variation': '0.23%'
    }


@patch.object(TokenAuthentication, 'authenticate_credentials')
@patch.object(IsAuthenticated, 'has_permission', return_value=True)
@patch('stock_market.controllers.stock_market.get_stock_data')
def test_stocks_api_call_fail_due_to_invalid_symbol(mock_get_stock_data, mock_permissions, mock_authentication):
    test_token = 'test_token'
    test_user = User(email='test@gmail.com', name='name', last_name='last_name')
    mock_authentication.return_value = (test_user, test_token)
    mock_get_stock_data.side_effect = InvalidSymbolError()

    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + test_token)
    response = client.get('/stocks/IMB')

    assert response.status_code == 400
    assert response.json() == {'error_code': 'INVALID_STOCK_SYMBOL'}


@patch.object(TokenAuthentication, 'authenticate_credentials')
@patch.object(IsAuthenticated, 'has_permission', return_value=False)
def test_stocks_api_call_fail_due_to_invalid_api_key(mock_permissions, mock_authentication):
    test_token = 'test_token'
    mock_authentication.side_effect = exceptions.AuthenticationFailed()

    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + test_token)
    response = client.get('/stocks/IMB')

    assert response.status_code == 401
    assert response.json() == {'detail': 'Incorrect authentication credentials.'}


@patch.object(TokenAuthentication, 'authenticate_credentials')
@patch.object(IsAuthenticated, 'has_permission', return_value=True)
@patch('stock_market.controllers.stock_market.get_stock_data')
def test_stocks_api_call_fail_with_throttling(mock_get_stock_data, mock_permissions, mock_authentication):
    test_token = 'test_token'
    test_user = User(email='test@gmail.com', name='name', last_name='last_name')
    mock_authentication.return_value = (test_user, test_token)
    mock_get_stock_data.side_effect = InvalidSymbolError()

    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + test_token)

    for i in range(4):
        client.get('/stocks/IMB')

    response = client.get('/stocks/IMB')

    assert response.status_code == 429
