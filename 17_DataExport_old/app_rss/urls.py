from django.urls import path

from app_rss.feeds import LatestNewsFeed

urlpatterns = [
    path("latest/news/", LatestNewsFeed()),
]