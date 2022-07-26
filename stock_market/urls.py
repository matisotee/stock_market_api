from django.urls import path
from stock_market.controllers.sign_up import SignUpAPIView
from stock_market.controllers.stock_market import StockMarketAPIView

urlpatterns = [
    path('sign_up/', SignUpAPIView.as_view()),
    path('stocks/<str:symbol>', StockMarketAPIView.as_view()),
]
