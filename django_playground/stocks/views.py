# Create your views here.
from django.urls import reverse
from django.utils.timezone import now
from django.views.generic import CreateView, TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from django_playground.stocks.forms import StockMovementForm
from django_playground.stocks.models import Product
from django_playground.stocks.models import StockMovement


class StockDashboard(TemplateView):
    template_name = "stocks/dashboard.html"


class StockListView(ListView):
    model = Product
    queryset = Product.objects.prefetch_related("category", "supplier").all()
    template_name = "stocks/products/list.html"
    paginate_by = 20



class StockDetailView(DetailView):
    model = Product
    template_name = "stocks/products/detail.html"

    def get_queryset(self):
        return Product.objects.prefetch_related("category", "supplier", "stock_movements").all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['stock_movements'] = self.object.stock_movements.all().order_by("-date")
        return context


# views.py
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.views.generic import FormView
from .models import Product
from .forms import ProductBurnForm


class ProductBurnView(FormView):
    template_name = "stocks/products/burn.html"
    form_class = ProductBurnForm
    success_url = reverse_lazy('stocks:products')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Gestion des exceptions pour le cas où le produit n'existe pas
        product = get_object_or_404(Product, pk=self.kwargs.get('pk'))
        context['product_name'] = product.name
        context['product_quantity'] = product.quantity_in_stock
        return context

    def form_valid(self, form):
        # Récupérer le produit correspondant à l'ID passé dans les kwargs
        product = get_object_or_404(Product, pk=self.kwargs.get('pk'))

        # Récupérer les données du formulaire
        quantity = form.cleaned_data['quantity']
        scheduled_date = form.cleaned_data['scheduled_date']
        reason = form.cleaned_data['reason']

        product.burn_stock(quantity, scheduled_date, reason)


        # Ajouter un message de succès
        messages.success(self.request, f'The stock burn task for {product.name} has been scheduled.')

        return super().form_valid(form)


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # TODO add a exception handling for the case when the product does not exist.
        context['product_name'] = Product.objects.get(pk=self.kwargs.get('pk')).name
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['pk'] = self.kwargs.get('pk')
        return kwargs
