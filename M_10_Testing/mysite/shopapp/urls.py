from django.urls import path

from .views import (
    ShopIndexView,
    GroupsListView,

    ProductDetailsView,
    ProductsListView,
    ProductsDataExportView,
    ProductCreateView,
    ProductUpdeteView,
    ProductArchiveView,

    OrdersListView,
    OrderDetailsView,
    OrdersDataExportView,
    OrderCreateView,
    OrderUpdeteView,
    OrderDeleteView,
)

app_name = "shopapp"

urlpatterns = [
    path("", ShopIndexView.as_view(), name="index"),
    path("groups/", GroupsListView.as_view(), name="groups_list"),
    path("products/", ProductsListView.as_view(), name="products_list"),
    path("products/export/", ProductsDataExportView.as_view(), name="products-export"),
    path("products/create/", ProductCreateView.as_view(), name="product_create"),
    path("products/<int:pk>/", ProductDetailsView.as_view(), name="product_details"),
    path("products/<int:pk>/update/", ProductUpdeteView.as_view(), name="product_update"),
    path("products/<int:pk>/archive/", ProductArchiveView.as_view(), name="product_archive"),

    path("orders/", OrdersListView.as_view(), name="orders_list"),
    path("orders/export/", OrdersDataExportView.as_view(), name="orders-export"),
    path("orders/create/", OrderCreateView.as_view(), name="order_create"),
    path("orders/<int:pk>/", OrderDetailsView.as_view(), name="order_details"),
    path("orders/<int:pk>/update/", OrderUpdeteView.as_view(), name="order_update"),
    path("orders/<int:pk>/delete-order/", OrderDeleteView.as_view(), name="order_delete"),
]
