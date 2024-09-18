from django.urls import path

from django_playground.stocks.views import StockDetailView, StockDashboard, ProductBurnView
from django_playground.stocks.views import StockListView
from django_playground.stocks.views import StockMovementCreateView
from django_playground.stocks.views import StockMovementListView

app_name = "stocks"
urlpatterns = [
    path("", view=StockDashboard.as_view(), name="stocks"),
    path("products/", view=StockListView.as_view(), name="products"),
    path("products/<slug:pk>/", view=StockDetailView.as_view(), name="product-detail"),
    path("products/<slug:pk>/burn/", view=ProductBurnView.as_view(), name="product-stock-burn"),
    path("products/<slug:pk>/new-movement/", view=StockMovementCreateView.as_view(), name="product-new-movement"),
    path("movements/", view=StockMovementListView.as_view(), name="stock-movements"),
]
