from django.contrib.auth.mixins import UserPassesTestMixin, PermissionRequiredMixin
from django.core import serializers
from django.http import (
    HttpResponse,
    HttpRequest,
    HttpResponseBadRequest
)
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView
from django.shortcuts import reverse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.viewsets import ModelViewSet

from .models import Article
from .forms import ArticleForm
from .serializers import ArticleSerializer


class ArticlesListView(ListView):
    """
    Представление для отображения статей
    Добавлкен миксин, проверяющий авторизован ли пользователь
    """
    template_name = "blogapp/article_list.html"
    context_object_name = "articles"
    queryset = (
        Article.objects
        .select_related("category")
        .select_related("author")
        .prefetch_related("tags")
        .defer('content')
    )


class ArticleCreateView(PermissionRequiredMixin, CreateView):
    """
    Представление для отображения формы по созданию новой статьи
    Добавлен миксин, проверяющие право пользователя на добавление статьи
    """

    permission_required = "blog_app.add_article"
    template_name = "blogapp/article_form.html"
    model = Article
    form_class = ArticleForm
    success_url = reverse_lazy("blogapp:articles")


class ArticleDetailsView(DetailView):
    """ Представление для детального отображения статьи """

    template_name = "blogapp/article-details.html"
    queryset = (
        Article.objects
        .select_related("author")
    )
    context_object_name = "article"


class ArticleUpdateView(UserPassesTestMixin, UpdateView):
    """
    Представление для отображения формы по редактированию стати
    Добавлен миксин, проверяющий доступ пользователя к редактированию статьи
    """

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


class ArticleViewSet(ModelViewSet):
    """
    Набор представлений для действий над Article
    Полный CRUD для сущностей статей
    """
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    filter_backends = [
        SearchFilter,
        DjangoFilterBackend,
        OrderingFilter,
    ]
    filterset_fields = [
        "title",
        "content",
        "author",
    ]
    ordering_fields = [
        "title",
        "pub_data",
        "category",
        "tags",
    ]


def get_articles_in_custom_format(request: HttpRequest) -> HttpResponse:
    format = request.GET['format']
    if format not in ['xml', 'json', 'yaml']:
        return HttpResponseBadRequest()
    data = serializers.serialize(format, Article.objects.all())
    return HttpResponse(data)
