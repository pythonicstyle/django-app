from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.generic import DetailView, ListView

from app_housing.models import Housing, NewsItem


class HousingListView(ListView):
    """
    Представление для отображения списка жилья
    """

    template_name = "app_housing/housing_list.html"
    context_object_name = "housing"
    queryset = (
        Housing.objects
        .select_related("type")
        .select_related("rooms")
        .defer("pub_data", "agent")
    )


class HouseDetailView(DetailView):
    """
    Представление для отображения детальной информации о жилье
    """
    model = Housing
    template_name = "app_housing/house_detail.html"


def about_us_info(request: HttpRequest) -> HttpResponse:
    """
    Представление для отоброжения информации о компании
    """

    return render(request, "app_housing/about_us.html")


class NewsItemListView(ListView):
    """
    Представление для отображения списка новостей
    """
    template_name = "app_housing/news_list.html"
    context_object_name = "news"
    queryset = NewsItem.objects.all()


class NewsItemDetailView(DetailView):
    """
    Представление для отображения новости
    """
    model = NewsItem
    template_name = "app_housing/newsitem_detail.html"
