from django.urls import path, include

from .views import (
    ArticlesListView,
    ArticleDetailsView,
    ArticleUpdateView,
    ArticleCreateView,
)

app_name = "blogapp"

urlpatterns = [
    path("articles/", ArticlesListView.as_view(), name="articles"),
    path("article/<int:pk>/", ArticleDetailsView.as_view(), name="article_details"),
    path("article/<int:pk>/edit/", ArticleUpdateView.as_view(), name="edit_article"),
    path("create-article/", ArticleCreateView.as_view(), name="article_create"),
]