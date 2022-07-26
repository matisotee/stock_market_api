from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from rest_framework import generics
from rest_framework.exceptions import ValidationError

from rest_framework.permissions import AllowAny

from stock_market.services.sign_up import sign_up, IncorrectPasswordError


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


class SignUpAPIView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = SignUpSerializer
