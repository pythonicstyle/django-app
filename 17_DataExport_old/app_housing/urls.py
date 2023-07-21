from django.urls import path

from app_housing.views import (
    about_us_info,
    HousingListView,
    HouseDetailView,
    NewsItemListView,
    NewsItemDetailView,
)

urlpatterns = [
    path("about_us/", about_us_info, name="about_us"),
    path("housing_list/", HousingListView.as_view(), name="housing_list"),
    path("housing/<int:pk>/", HouseDetailView.as_view(), name="house_details"),
    path("news/", NewsItemListView.as_view(), name="news"),
    path("news-item/<int:pk>/", NewsItemDetailView.as_view(), name="news-item"),
]
