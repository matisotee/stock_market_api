from unittest.mock import patch
import pytest
from stock_market.models import User
from rest_framework.authtoken.models import Token
from stock_market.models.user import UserManager
from stock_market.services.sign_up import sign_up, IncorrectPasswordError


@patch.object(Token, 'objects')
@patch.object(User, 'save')
@patch.object(User, 'set_password')
@patch.object(UserManager, 'get')
def test_sign_up_successfully_with_new_user(mock_get_user, mock_set_password, mock_save, mock_token_objects):
    mock_get_user.side_effect = User.DoesNotExist()
    mock_token_objects.create.return_value = 'test_token'

    result = sign_up(
        email='test@email.com',
        name='Test',
        last_name='Name',
        password='1234test'
    )

    mock_set_password.assert_called_once_with('1234test')
    mock_save.assert_called_once()
    mock_token_objects.create.assert_called_once()
    assert result.email == 'test@email.com'
    assert result.name == 'Test'
    assert result.last_name == 'Name'
    assert result.api_key == 'test_token'


@patch.object(Token, 'objects')
@patch.object(User, 'check_password')
@patch.object(UserManager, 'get')
def test_sign_up_successfully_with_existent_user(mock_get_user, mock_check_password, mock_token_objects):
    email = 'test@email.com'
    name = 'Test'
    last_name = 'Name'
    password = '1234test'
    api_key = 'test_token'

    mock_get_user.return_value = User(email=email, name=name, last_name=last_name)
    mock_check_password.return_value = True
    mock_token_objects.get.return_value = api_key

    result = sign_up(
        email=email,
        name=name,
        last_name=last_name,
        password=password
    )

    mock_get_user.assert_called_once_with(email=email)
    mock_check_password.assert_called_once_with(password)
    mock_token_objects.get.assert_called_once()
    assert result.email == email
    assert result.name == name
    assert result.last_name == last_name
    assert result.api_key == api_key


@patch.object(User, 'check_password')
@patch.object(UserManager, 'get')
def test_sign_up_failed_with_incorrect_password(mock_get_user, mock_check_password):
    email = 'test@email.com',
    name = 'Test',
    last_name = 'Name',
    password = '1234test'
    api_key = 'test_token'

    mock_get_user.return_value = User(email=email, name=name, last_name=last_name)
    mock_check_password.return_value = False

    with pytest.raises(IncorrectPasswordError):
        sign_up(
            email=email,
            name=name,
            last_name=last_name,
            password=password
        )

    mock_get_user.assert_called_once_with(email=email)
    mock_check_password.assert_called_once_with(password)
