from django.urls import path
from stock_market.controllers.sign_up import SignUpAPIView
from stock_market.controllers.stock_market import StockMarketAPIView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(title="Stock Market API", default_version='v1'),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('sign_up/', SignUpAPIView.as_view()),
    path('stocks/<str:symbol>', StockMarketAPIView.as_view()),
]
