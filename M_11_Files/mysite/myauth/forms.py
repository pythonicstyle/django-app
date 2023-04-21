from django import forms

from .models import User


class UserUpdateForm(forms.ModelForm):
    avatar = forms.ImageField(required=False)
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'avatar']
