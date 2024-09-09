from django.urls import path

from django_playground.stocks.views import StockListView
from django_playground.stocks.views import StockMovementListView

app_name = "stocks"
urlpatterns = [
    path("", view=StockListView.as_view(), name="stocks"),
    path("movements/", view=StockMovementListView.as_view(), name="stock-movements"),
]
