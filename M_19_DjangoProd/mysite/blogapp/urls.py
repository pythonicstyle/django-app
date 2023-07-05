from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (
    ArticlesListView,
    ArticleDetailsView,
    ArticleUpdateView,
    ArticleCreateView,
    ArticleViewSet,
    LatestArticlesFeed,
)

app_name = "blogapp"

routers = DefaultRouter()
routers.register("products", ArticleViewSet)

urlpatterns = [
    path("articles/", ArticlesListView.as_view(), name="articles"),
    path("article/<int:pk>/", ArticleDetailsView.as_view(), name="article_details"),
    path("articles/latest/feed/", LatestArticlesFeed(), name="articles-feed"),
    path("article/<int:pk>/edit/", ArticleUpdateView.as_view(), name="edit_article"),
    path("create-article/", ArticleCreateView.as_view(), name="article_create"),
]
