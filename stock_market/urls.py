from django.urls import path
from stock_market.controllers.sign_up import SignUpAPIView

urlpatterns = [
    path('sign_up/', SignUpAPIView.as_view()),
]
