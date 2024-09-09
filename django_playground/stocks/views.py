# Create your views here.
from django.views.generic.list import ListView

from django_playground.stocks.models import Product
from django_playground.stocks.models import StockMovement


class StockListView(ListView):
    model = Product
    template_name = "stocks/all_stocks.html"
    context_object_name = "products"


class StockMovementListView(ListView):
    model = StockMovement
    template_name = "stocks/stock_movements.html"
    context_object_name = "stock_movements"
