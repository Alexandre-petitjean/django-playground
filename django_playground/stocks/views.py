from datetime import timedelta

from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.urls import reverse
from django.urls import reverse_lazy
from django.utils.timezone import now
from django.views import View
from django.views.generic import CreateView
from django.views.generic import FormView
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from django_playground.stocks.forms import ProductBurnForm
from django_playground.stocks.forms import ProductOrderForm
from django_playground.stocks.forms import StockMovementForm
from django_playground.stocks.models import Product
from django_playground.stocks.models import StockMovement


class StockDashboard(TemplateView):
    template_name = "stocks/dashboard.html"


class StockListView(ListView):
    model = Product
    template_name = "stocks/products/list.html"
    paginate_by = 20


class ProductsBurnAllStockView(View):
    success_url = reverse_lazy("stocks:products")

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        midnight = now().replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)
        products = Product.objects.all()
        for product in products:
            product.burn_stock(quantity=product.stock, scheduled_date=midnight, reason="Burn all stock")

        messages.success(request, f"The stock of {len(products)} products is scheduled to burn at midnight.")

        return redirect(self.success_url)


class ProductDetailView(DetailView):
    model = Product
    template_name = "stocks/products/detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["stock_movements"] = self.object.stock_movements.all().order_by("-created_at")[:10]
        return context


class ProductBurnFormView(FormView):
    template_name = "stocks/products/burn.html"
    form_class = ProductBurnForm
    success_url = reverse_lazy("stocks:products")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = get_object_or_404(Product, pk=self.kwargs.get("pk"))
        context["product_name"] = product.title
        context["product_quantity"] = product.stock
        return context

    def form_valid(self, form):
        product = get_object_or_404(Product, pk=self.kwargs.get("pk"))

        quantity = form.cleaned_data["quantity"]
        scheduled_date = form.cleaned_data["scheduled_date"]
        reason = form.cleaned_data["reason"]
        product.burn_stock(quantity, scheduled_date, reason)

        messages.success(self.request, f"The stock burn task for {product.title} has been scheduled.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("stocks:product-detail", kwargs={"pk": self.kwargs.get("pk")})


class ProductOrderFormView(FormView):
    template_name = "stocks/products/order.html"
    form_class = ProductOrderForm
    success_url = reverse_lazy("stocks:products")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = get_object_or_404(Product, pk=self.kwargs.get("pk"))
        context["product_name"] = product.title
        return context

    def form_valid(self, form):
        product = get_object_or_404(Product, pk=self.kwargs.get("pk"))

        quantity = form.cleaned_data["quantity"]
        scheduled_date = form.cleaned_data["scheduled_date"]
        reason = form.cleaned_data["reason"]
        product.order_stock(quantity, scheduled_date, reason)

        messages.success(self.request, f"Order {quantity} of unit for {product.title} has been scheduled.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("stocks:product-detail", kwargs={"pk": self.kwargs.get("pk")})


class StockMovementCreateView(CreateView):
    model = StockMovement
    form_class = StockMovementForm
    template_name = "stocks/movements/form.html"

    def get_success_url(self):
        return reverse("stocks:product-detail", kwargs={"pk": self.object.product.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # TODO add a exception handling for the case when the product does not exist.
        context["product_name"] = Product.objects.get(pk=self.kwargs.get("pk")).name
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["pk"] = self.kwargs.get("pk")
        return kwargs


class StockMovementListView(ListView):
    model = StockMovement
    queryset = StockMovement.objects.prefetch_related("product").all()
    template_name = "stocks/movements/list.html"
    paginate_by = 20
