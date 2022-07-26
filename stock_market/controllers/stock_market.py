from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from stock_market.controllers.utils import TokenAuthentication
from stock_market.services.stock_market import get_stock_data, InvalidSymbolError
from rest_framework.permissions import IsAuthenticated


class StockMarketSerializer(serializers.Serializer):
    open_price = serializers.CharField(
        read_only=True
    )
    higher_price = serializers.CharField(
        read_only=True
    )
    lower_price = serializers.CharField(
        read_only=True
    )
    close_price_variation = serializers.CharField(
        read_only=True
    )


class StockMarketAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get(self, request, symbol):
        try:
            response = get_stock_data(symbol)
        except InvalidSymbolError:
            raise ValidationError({"error_code": "INVALID_STOCK_SYMBOL"})

        serializer = StockMarketSerializer(response)
        return Response(serializer.data)
