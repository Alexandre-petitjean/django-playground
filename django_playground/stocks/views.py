# Create your views here.
from django.urls import reverse
from django.views.generic import CreateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from django_playground.stocks.forms import StockMovementForm
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


class StockMovementCreateView(CreateView):
    model = StockMovement
    form_class = StockMovementForm
    template_name = "stocks/movements/form.html"

    def get_success_url(self):
        return reverse("stocks:product-detail", kwargs={"pk": self.object.product.pk})
