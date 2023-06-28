from django import forms
from django.contrib.auth.models import Group

from .models import Product, Order


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = "name",


class ProductForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['created_by'].empty_label = "None"
        self.fields['created_by'].label = "Created by"
        self.fields['created_by'].required = True

    class Meta:
        model = Product
        fields = ["name", "price", "description", "discount", "created_by", "preview"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-input"}),
            "description": forms.Textarea(attrs={"cols": 30, "rows": 5}),
        }

    # images = forms.ImageField(
    #     widget=forms.ClearableFileInput(attrs={"multiple": True}),
    # )


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


class CSVImportForm(forms.Form):
    csv_file = forms.FileField()
