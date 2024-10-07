from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.urls import reverse_lazy
from django.views.generic import FormView

from django_playground.stocks.models import Product


class ProductFormViewMixin(FormView):
    template_name = "stocks/products/form-send-order.html"
    form_class = None
    success_url = reverse_lazy("stocks:products")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = get_object_or_404(Product, pk=self.kwargs.get("pk"))
        context["product"] = product
        return context

    def get_success_url(self):
        return reverse("stocks:product-detail", kwargs={"pk": self.kwargs.get("pk")})
