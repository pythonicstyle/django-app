from django.contrib.auth.mixins import UserPassesTestMixin, PermissionRequiredMixin
from django.contrib.syndication.views import Feed
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, DetailView, UpdateView
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
        .order_by('-pub_data')
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


# def get_articles_in_custom_format(request: HttpRequest) -> HttpResponse:
#     format = request.GET['format']
#     if format not in ['xml', 'json', 'yaml']:
#         return HttpResponseBadRequest()
#     data = serializers.serialize(format, Article.objects.all())
#     return HttpResponse(data)


class LatestArticlesFeed(Feed):  # RSS лента
    """ Представление для отображения ленты новостей """

    title = "Blog articles (latest)"
    description = "updates on changes and additions blog articles"
    link = reverse_lazy("blogapp:articles")

    def items(self):  # получение информации о статьях, которые мы хотим отобразить в списке ленты
        return (
            Article.objects
            .filter(is_published=True)
            .order_by('-pub_data')[:5]  # загрузка последних 5 статей
        )

    def item_title(self, item: Article):  # метод возвращает заголовок из объекта в списке
        return item.title

    def item_description(self, item: Article):  # передает информацию о том объекте, о котором вышла статья
        return item.content[:200]

    def item_link(self, item: Article):  # метод генериркет ссылку, чтобы пользователь мог перейти на сайт по ссылке
        return reverse("blogapp:article_details", kwargs={"pk": item.pk})
