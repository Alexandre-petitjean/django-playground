from django import forms
from django.forms import ModelForm

from django_playground.stocks.models import StockMovement


class StockMovementForm(ModelForm):
    class Meta:
        model = StockMovement
        fields = ["product", "movement_type", "quantity", "description"]
        widgets = {
            "product": forms.HiddenInput(),
            "movement_type": forms.RadioSelect(),
        }
