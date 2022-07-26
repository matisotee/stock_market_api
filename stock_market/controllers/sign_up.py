from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from rest_framework import generics
from rest_framework.exceptions import ValidationError

from rest_framework.permissions import AllowAny

from stock_market.services.sign_up import sign_up, IncorrectPasswordError
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.utils.decorators import method_decorator


class SignUpSerializer(serializers.Serializer):
    email = serializers.EmailField(
        required=True,
    )
    name = serializers.CharField(
        required=False,
    )
    last_name = serializers.CharField(
        required=False,
    )
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password]
    )
    api_key = serializers.CharField(
        read_only=True,
    )

    def create(self, validated_data):
        try:
            response = sign_up(
                email=validated_data['email'],
                password=validated_data['password'],
                name=validated_data['name'],
                last_name=validated_data['last_name']
            )
        except IncorrectPasswordError:
            raise ValidationError({"error_code": "INCORRECT_PASSWORD"})

        return response


@method_decorator(name='post', decorator=swagger_auto_schema(
    request_body=SignUpSerializer,
    responses={
        201: openapi.Response(
            description='',
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'email': openapi.Schema(type=openapi.TYPE_STRING),
                    'name': openapi.Schema(type=openapi.TYPE_STRING),
                    'last_name': openapi.Schema(type=openapi.TYPE_STRING),
                    'api_key': openapi.Schema(type=openapi.TYPE_STRING),
                }
            )
        ),
    }
))
class SignUpAPIView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = SignUpSerializer
