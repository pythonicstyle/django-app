from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (
    ArticlesListView,
    ArticleDetailsView,
    ArticleUpdateView,
    ArticleCreateView,
    get_articles_in_custom_format,
    ArticleViewSet,
)

app_name = "blogapp"

routers = DefaultRouter()
routers.register("products", ArticleViewSet)

urlpatterns = [
    path("articles/", ArticlesListView.as_view(), name="articles"),
    path("article/<int:pk>/", ArticleDetailsView.as_view(), name="article_details"),
    path("article/<int:pk>/edit/", ArticleUpdateView.as_view(), name="edit_article"),
    path("create-article/", ArticleCreateView.as_view(), name="article_create"),
    # path("", get_articles_in_custom_format, name="articles"),
]
