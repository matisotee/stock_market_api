from stock_market.models import User
from rest_framework.authtoken.models import Token


def sign_up(email, name, last_name, password):

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        user = User.objects.create_user(
            email=email,
            password=password,
            name=name,
            last_name=last_name
        )
        user.api_key = Token.objects.create(user=user)
        return user

    if not user.check_password(password):
        raise IncorrectPasswordError()

    user.api_key = Token.objects.get(user=user)
    return user


class IncorrectPasswordError(Exception):
    pass

