from django import forms
from django.core import validators
from django.contrib.auth.models import User


from .models import Product, Order


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields =["name", "price", "description", "discount"]
        widgets = {
            "description": forms.Textarea(attrs={"cols": 30, "rows": 5}),
            # "discount": forms.DecimalField(max_value="99")
        }


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["user", "products", "delivery_address", "promocode"]
        widgets = {
            "user": forms.TextInput(attrs={'class': 'form-input'}),
            # "products": forms.ModelChoiceField(queryset=Product.objects.all())
        }

# class ProductForm(forms.Form):
#     name = forms.CharField(max_length=100)
#     price = forms.DecimalField(min_value=1, max_value=100000, decimal_places=2)
#     description = forms.CharField(
#         label="Product description",
#         widget=forms.Textarea(attrs={"rows": 5, "cols": 30}),
#         validators=[validators.RegexValidator(
#             regex="great",
#             message="Field must contain word 'great'",
#         )]
#     )
#     discount = forms.DecimalField(min_value=0, max_value=99)


# class OrderForm(forms.Form):
#     user = Order.user
#     promocode = forms.CharField(max_length=20, required=False)
#     delivery_address = forms.CharField()
#     products = forms.ModelChoiceField(Product.objects.all(), label="Choose product")
#     count = forms.IntegerField(min_value=1, max_value=10)
