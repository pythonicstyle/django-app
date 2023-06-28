from django import forms

from .models import Article


class ArticleForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['author'].empty_label = "None"
        self.fields['author'].label = "Created by"
        self.fields['author'].required = True
        self.fields['category'].empty_label = "None"

    class Meta:
        model = Article
        fields = ["title", "content", "author", "category", "tags"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-input"}),
            "content": forms.Textarea(attrs={"cols": 40, "rows": 10}),
            "tags": forms.CheckboxSelectMultiple(attrs={"input type": "checkbox"})
        }
