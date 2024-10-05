from django.urls import path

from django_playground.stocks.views import ProductDetailView
from django_playground.stocks.views import ProductOrderFormView
from django_playground.stocks.views import ProductsSendAllView
from django_playground.stocks.views import SendProductFormView
from django_playground.stocks.views import StockDashboard
from django_playground.stocks.views import StockListView
from django_playground.stocks.views import StockMovementCreateView
from django_playground.stocks.views import StockMovementListView

app_name = "stocks"
urlpatterns = [
    path("", view=StockDashboard.as_view(), name="stocks"),
    path("products/", view=StockListView.as_view(), name="products"),
    path("products/send-all/", view=ProductsSendAllView.as_view(), name="products-send-all"),
    path("products/<slug:pk>/", view=ProductDetailView.as_view(), name="product-detail"),
    path("products/<slug:pk>/send/", view=SendProductFormView.as_view(), name="product-send"),
    path("products/<slug:pk>/order/", view=ProductOrderFormView.as_view(), name="product-order"),
    path("products/<slug:pk>/new-movement/", view=StockMovementCreateView.as_view(), name="product-new-movement"),
    path("movements/", view=StockMovementListView.as_view(), name="stock-movements"),
]
