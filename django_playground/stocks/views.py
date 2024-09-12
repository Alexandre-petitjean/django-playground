# Create your views here.
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from django_playground.stocks.models import Product
from django_playground.stocks.models import StockMovement


class StockListView(ListView):
    model = Product
    queryset = Product.objects.prefetch_related("category", "supplier").all()
    template_name = "stocks/products/list.html"
    paginate_by = 20


class StockDetailView(DetailView):
    model = Product
    template_name = "stocks/products/detail.html"


class StockMovementListView(ListView):
    model = StockMovement
    queryset = StockMovement.objects.prefetch_related("product").all()
    template_name = "stocks/movements/list.html"
    paginate_by = 20
