from unittest.mock import patch
from rest_framework.test import APIClient

from stock_market.models import User
from stock_market.services.sign_up import IncorrectPasswordError


@patch('stock_market.controllers.sign_up.sign_up')
def test_sign_up_api_call_successful(mock_sign_up):
    email = 'test@gmail.com'
    name = 'Test'
    last_name = 'Name'
    password = '1234test'
    api_key = 'test_token'

    user = User(email=email, name=name, last_name=last_name)
    user.api_key = api_key
    mock_sign_up.return_value = user

    client = APIClient()
    response = client.post(
        '/sign_up/',
        {
            'email': email,
            'name': name,
            'last_name': last_name,
            'password': password
        },
        format='json'
    )

    assert response.status_code == 201
    assert response.data == {'email': email, 'name': name, 'last_name': last_name, 'api_key': api_key}


@patch('stock_market.controllers.sign_up.sign_up')
def test_sign_up_api_call_failed(mock_sign_up):
    email = 'test@gmail.com'
    name = 'Test'
    last_name = 'Name'
    password = '1234test'

    mock_sign_up.side_effect = IncorrectPasswordError()

    client = APIClient()
    response = client.post(
        '/sign_up/',
        {
            'email': email,
            'name': name,
            'last_name': last_name,
            'password': password
        },
        format='json'
    )

    assert response.status_code == 400
    assert response.json() == {'error_code': 'INCORRECT_PASSWORD'}


@patch('stock_market.controllers.sign_up.sign_up')
def test_sign_up_api_call_fail_with_throttling(mock_sign_up):
    email = 'test@gmail.com'
    name = 'Test'
    last_name = 'Name'
    password = '1234test'
    api_key = 'test_token'

    user = User(email=email, name=name, last_name=last_name)
    user.api_key = api_key
    mock_sign_up.return_value = user

    client = APIClient()

    for i in range(4):
        client.post(
            '/sign_up/',
            {
                'email': email,
                'name': name,
                'last_name': last_name,
                'password': password
            },
            format='json'
        )

    response = client.post(
        '/sign_up/',
        {
            'email': email,
            'name': name,
            'last_name': last_name,
            'password': password
        },
        format='json'
    )

    assert response.status_code == 429
