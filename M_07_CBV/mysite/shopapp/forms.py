from django import forms
from django.contrib.auth.models import Group

from .models import Product, Order


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = "name",


class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ["name", "price", "description", "discount"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-input"}),
            "description": forms.Textarea(attrs={"cols": 30, "rows": 5}),
        }


class OrderForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user'].empty_label = "None"

    class Meta:
        model = Order
        fields = ["user", "products", "delivery_address", "promocode"]
        labels = {
            "user": "Name",
            "products": "Choose products",
        }
        widgets = {
            "delivery_address": forms.Textarea(attrs={"cols": 30, "rows": 1}),
            "products": forms.CheckboxSelectMultiple(attrs={"input type": "checkbox"})
        }

