from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from django.forms import ModelForm, Form

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
        self.helper.form_id = 'form-stock-movement'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit'))

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.product_id = self.product_id
        if commit:
            instance.save()
        return instance


class ProductBurnForm(Form):
    quantity = forms.IntegerField(
        required=False,
        help_text="Quantity to burn, if not specified all the stock will be burned."
    )
    scheduled_date = forms.DateField(
        required=False,
        help_text="Date when the stock will be burned. If not specified, the stock will be burned immediately."
    )
    reason = forms.CharField(widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'form-product-burn'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit'))

