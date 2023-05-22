from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView
from django.shortcuts import render, redirect, reverse

from .models import Article
from .forms import ArticleForm


class ArticlesListView(ListView):
    template_name = "blogapp/article_list.html"
    context_object_name = "articles"
    queryset = (
        Article.objects
        .select_related("category")
        .select_related("author")
        .prefetch_related("tags")
        # TODO стоит добавить исключение поля которое не требуется, а ведь оно может содержать большой объем данных:
        #  .defer('content')
    )


class ArticleCreateView(CreateView):
    template_name = "blogapp/article_form.html"
    model = Article
    form_class = ArticleForm
    success_url = reverse_lazy("blogapp:articles")


class ArticleDetailsView(DetailView):
    template_name = "blogapp/article-details.html"
    queryset = (
        Article.objects
        .select_related("author")
    )
    context_object_name = "article"


class ArticleUpdateView(UserPassesTestMixin, UpdateView):
    def test_func(self):
        return self.request.user == self.get_object().author \
            and self.request.user.has_perm("blogapp.change_article") \
            or self.request.user.is_superuser

    model = Article
    form_class = ArticleForm
    template_name = "blogapp/article_update_form.html"

    def get_success_url(self):
        return reverse(
            "blogapp:article_details",
            kwargs={"pk": self.object.pk},
        )

    def form_valid(self, form):
        response = super().form_valid(form)
        return response
