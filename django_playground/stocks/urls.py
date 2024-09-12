from django.urls import path

from django_playground.stocks.views import StockDetailView
from django_playground.stocks.views import StockListView
from django_playground.stocks.views import StockMovementCreateView
from django_playground.stocks.views import StockMovementListView

app_name = "stocks"
urlpatterns = [
    path("", view=StockListView.as_view(), name="stocks"),
    path("products/<slug:pk>/", view=StockDetailView.as_view(), name="product-detail"),
    path("movements/", view=StockMovementListView.as_view(), name="stock-movements"),
    path("products/<slug:pk>/new-movement/", view=StockMovementCreateView.as_view(), name="stock-movements-new"),
]
