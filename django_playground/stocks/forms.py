from datetime import timedelta

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from django.core.validators import MinValueValidator
from django.forms import Form
from django.forms import ModelForm
from django.utils import timezone

from django_playground.stocks.models import StockMovement


class StockMovementForm(ModelForm):
    class Meta:
        model = StockMovement
        fields = ["movement_type", "quantity", "description"]
        widgets = {
            "product": forms.HiddenInput(),
            "movement_type": forms.RadioSelect(),
        }

    def __init__(self, *args, **kwargs):
        pk = kwargs.pop("pk")
        super().__init__(*args, **kwargs)
        self.product_id = pk
        self.helper = FormHelper()
        self.helper.form_id = "form-stock-movement"
        self.helper.form_method = "post"
        self.helper.add_input(Submit("submit", "Submit", css_class="btn btn-success btn-lg"))

    def save(self, commit=True):  # noqa: FBT002
        instance = super().save(commit=False)
        instance.product_id = self.product_id
        if commit:
            instance.save()
        return instance


class ProductStockForm(Form):
    quantity = forms.IntegerField(required=False, initial=10)
    scheduled_date = forms.DateTimeField(
        required=False,
        widget=forms.DateInput(attrs={"type": "datetime-local"}),
        initial=timezone.now() + timedelta(minutes=1),
        validators=[MinValueValidator(timezone.now())],
    )
    reason = forms.CharField(widget=forms.Textarea, initial="No reason provided.")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = "form-product-stock"
        self.helper.form_method = "post"
        self.helper.add_input(Submit("submit", "Submit", css_class="btn btn-success btn-lg"))


class ProductSendForm(ProductStockForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["quantity"].help_text = "Quantity to send, if not specified all the stock will be sent."
        self.fields[
            "scheduled_date"
        ].help_text = "Date when the stock will be send. If not specified, the stock will be sent immediately."
        self.fields["reason"].initial = "Stock sent to customer."


class ProductOrderForm(ProductStockForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["quantity"].help_text = "Quantity to order, must be superior or equal to 1."
        self.fields["quantity"].validators = [MinValueValidator(1)]
        self.fields[
            "scheduled_date"
        ].help_text = "Date when the stock will be order. If not specified, the stock will be ordered immediately."
        self.fields["reason"].initial = "Simple restock."
