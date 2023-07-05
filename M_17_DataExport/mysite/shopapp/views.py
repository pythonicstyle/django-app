""" Разные view для интернет-магазина: по товарам, заказам и т. д. """
from csv import DictWriter
from timeit import default_timer
import logging

from django.contrib.auth.models import Group, User
from django.core.cache import cache
from django.http import (
    HttpResponse,
    HttpRequest,
    HttpResponseRedirect,
    JsonResponse
)
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views import *
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.urls import reverse_lazy
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
    UserPassesTestMixin
)
from rest_framework.parsers import MultiPartParser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, OpenApiResponse

from .common import save_scv_products
from .forms import ProductForm, OrderForm, GroupForm
from .models import Product, Order, ProductImage
from .serializers import ProductSerializer, OrderSerializer

logger = logging.getLogger(__name__)


# @extend_schema(description="Product views CRUD")
class ProductViewSet(ModelViewSet):
    """
    Набор представлений для действий над Product
    Полный CRUD для сущностей товара
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [
        SearchFilter,
        DjangoFilterBackend,
        OrderingFilter,
    ]
    search_fields = ["name", "description"]
    filterset_fields = [
        "name",
        "description",
        "price",
        "discount",
        "archived",
        "created_by",
    ]
    ordering_fields = [
        "name",
        "price",
        "discount",
    ]

    @extend_schema(
        summary="Get one product by ID",
        description="Retrieves **product**, returns 404 if not found",
        responses={
            200: ProductSerializer,
            404: OpenApiResponse(description="Empty response, product by ID not found"),
        }
    )
    def retrieve(self, *args, **kwargs):
        return super().retrieve(*args, **kwargs)

    @action(methods=["get"], detail=False)
    def download_CSV(self, request: Request):
        response = HttpResponse(content_type="text/csv")
        filename = "products-export.csv"
        response["Content-Description"] = f"attachment; filname={filename}"
        queryset = self.filter_queryset(self.get_queryset())
        fields = [
            "name",
            "description",
            "price",
            "discount",
        ]
        queryset = queryset.only(*fields)
        writer = DictWriter(response, fieldnames=fields)
        writer.writeheader()

        for product in queryset:
            writer.writerow({
                field: getattr(product, field)
                for field in fields
            })
        return response

    @action(
        detail=False,
        methods=["post"],
        parser_classes=[MultiPartParser]
    )
    def upload_csv(self, request: Request) -> Response:
        products = save_scv_products(
            request.FILES["file"].file,
            encoding=request.encoding,
        )
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)


class OrderViewSet(ModelViewSet):
    """
    Набор представлений для действий над Order
    Полный CRUD для сущностей товара
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filter_backends = [
        SearchFilter,
        DjangoFilterBackend,
        OrderingFilter,
    ]
    filterset_fields = [
        "delivery_address",
        "promocode",
        "user",
    ]
    ordering_fields = [
        "created_at",
        "delivery_address",
    ]


class ShopIndexView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        products = [
            ('Laptop', 1999),
            ('Desktop', 2999),
            ('Smartphone', 999),
        ]
        context = {
            "time_running": default_timer(),
            "products": products,
        }
        return render(request, 'shopapp/shop-index.html', context=context)


class GroupsListView(View):
    """
    Представление для отображения всех созданных групп
    """

    def get(self, request: HttpRequest) -> HttpResponse:
        context = {
            "form": GroupForm(),
            "groups": Group.objects.prefetch_related('permissions').all(),
        }
        return render(request, 'shopapp/groups-list.html', context=context)

    def post(self, request: HttpRequest) -> HttpResponse:
        form = GroupForm(request.POST)
        if form.is_valid():
            form.save()

        return redirect(request.path)


class ProductDetailsView(DetailView):
    """ Представление для детального отображения товара """

    template_name = "shopapp/products-details.html"
    queryset = Product.objects.prefetch_related("images")
    context_object_name = "product"


class ProductsListView(ListView):
    """ Представление для отображения списка товаров """

    template_name = "shopapp/products-list.html"
    context_object_name = "products"
    queryset = Product.objects.filter(archived=False)

    def get(self, request, **kwargs):
        logger.info("Запрошена страница со списком товаров")
        return super().get(request, **kwargs)


class ProductCreateView(PermissionRequiredMixin, CreateView):
    """
    Представление для отображения формы по созданию нового товара
    Добавлен миксин, проверяющие право пользователя на добавление товара
    """
    permission_required = "shopapp.add_product"
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy("shopapp:products_list")

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        logger.info(f"Пользователь {form.instance.created_by} создал новый продукт")
        return super().form_valid(form)


class ProductUpdateView(UserPassesTestMixin, UpdateView):
    """
    Представление для отображения формы по редактированию товара
    Добавлен миксин, проверяющий доступ пользователя к редактированию товара
    """

    def test_func(self):
        return self.request.user == self.get_object().created_by \
            and self.request.user.has_perm("shopapp.change_product") \
            or self.request.user.is_superuser

    model = Product
    form_class = ProductForm
    template_name_suffix = "_update_form"

    def get_success_url(self):
        return reverse(
            "shopapp:product_details",
            kwargs={"pk": self.object.pk},
        )

    def form_valid(self, form):
        response = super().form_valid(form)
        for image in form.files.getlist("images"):
            ProductImage.objects.create(
                product=self.object,
                image=image,
            )
        return response


class ProductArchiveView(DeleteView):
    """ Представление для отображения формы подтверждения добавления товара в архив """

    model = Product
    success_url = reverse_lazy("shopapp:products_list")

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.archived = True
        self.object.save()
        logger.info(f"Товар был добавлен в архив пользователем {self.request.user}")
        return HttpResponseRedirect(success_url)


class OrdersListView(LoginRequiredMixin, ListView):
    """
    Представление для отображения списка заказов
    Добавлкен миксин, проверяющий авторизован ли пользователь
    """

    queryset = (
        Order.objects
        .select_related("user")
        .prefetch_related("products")
    )
    template_name = "shopapp/orders_list.html"


class OrderDetailsView(PermissionRequiredMixin, DetailView):
    """
    Представление для детального отображения заказа
    Добавлен миксин, проверяющий доступ пользователя к просмотру заказов
    """
    permission_required = "view_order"
    template_name = "shopapp/order_details.html"
    queryset = (
        Order.objects
        .select_related("user")
        .prefetch_related("products")
    )


class OrderCreateView(CreateView):
    """ Представление для отображения формы для создания нового заказа """

    model = Order
    form_class = OrderForm
    success_url = reverse_lazy("shopapp:orders_list")

    def post(self, request, **kwargs):
        logger.info(f"{self.request.user} создал новый заказ")
        return super().get(request, **kwargs)


class OrderUpdateView(UserPassesTestMixin, UpdateView):
    """
    Представление для отображения формы редактирования товара
    Добавлен миксин, проверяющий статус модератора сайта
    и сравнивающий пользователя с автором заказа
    """

    def test_func(self):
        return self.request.user == self.get_object().created_by \
            and self.request.user.has_perm("shopapp.change_order") \
            or self.request.user.is_superuser

    model = Order
    form_class = OrderForm
    template_name_suffix = "_update_form"

    def get_success_url(self):
        return reverse(
            "shopapp:order_details",
            kwargs={"pk": self.object.pk},
        )


class OrderDeleteView(UserPassesTestMixin, DeleteView):
    """
    Представление для отображения формы подтверждения удаления заказа
    Добавлен миксин, проверяющий статус модератора сайта
    и сравнивающий пользователя с автором заказа

    """

    def test_func(self):
        return self.request.user == self.get_object().created_by \
            and self.request.user.has_perm("shopapp.delete_order") \
            or self.request.user.is_superuser

    model = Order
    success_url = reverse_lazy("shopapp:orders_list")

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.delete()
        logger.info(f"Заказ {self.request.pk} был удален пользователем {self.request.user}")

        return HttpResponseRedirect(success_url)


class ProductsDataExportView(View):
    """ Представление для выгрузки всех товаров в отдельный файл """

    def get(self, request: HttpRequest) -> JsonResponse:
        cache_key = "products_data_export"
        products_data = cache.get(cache_key)
        if products_data is None:
            products = Product.objects.order_by("pk").all()
            products_data = [
                {
                    "pk": product.pk,
                    "name": product.name,
                    "price": product.price,
                    "archived": product.archived,
                    "created by": product.created_by_id,
                }
                for product in products
            ]
            cache.set(cache_key, products_data, 60 * 5)
        return JsonResponse({"products": products_data})


class OrdersDataExportView(UserPassesTestMixin, View):
    """
    Представление для выгрузки всех заказов в отдельный файл
    Добавлен миксин, проверяющий статус модератора сайта
    """

    def test_func(self):
        return self.request.user.is_staff

    def get(self, request: HttpRequest) -> JsonResponse:
        cache_key = "orders_data_export"
        orders_data = cache.get(cache_key)
        if orders_data is None:
            orders = Order.objects.order_by("pk").all()
            orders_data = [
                {
                    "pk": order.pk,
                    "delivery_address": order.delivery_address,
                    "promocode": order.promocode,
                    "user": order.user_id,
                    "products": [product.pk for product in order.products.all()],
                }
                for order in orders
            ]
            cache.set(cache_key, orders_data, 60 * 5)

        return JsonResponse({"orders": orders_data})


class UserOrdersListView(UserPassesTestMixin, ListView):
    """
    Представление для отображения списка заказов пользователя
    Добавлен миксин, проверяющий авторизован ли пользователь
    """

    template_name = "shopapp/user_orders.html"

    def test_func(self):
        return self.request.user.is_authenticated

    def get_queryset(self):
        self.owner = User.objects.get(pk=self.kwargs["user_id"])
        self.user_orders = Order.objects\
            .filter(user=self.owner.id) \
            .order_by("created_at") \
            .all()

        for order in self.user_orders:
            print(order.pk)
        return self.user_orders

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["owner"] = self.owner
        context["user_orders_qs"] = self.user_orders
        return context


class UserOrdersDataExportView(UserPassesTestMixin, View):
    """
    Представление для выгрузки всех заказов пользователя в отдельный JSON-файл
    Добавлен миксин, проверяющий статус модератора сайта
    """

    def test_func(self):
        return self.request.user.is_staff

    def get_queryset(self):
        self.owner = User.objects.get(pk=self.kwargs["user_id"])
        return Order.objects.filter(user=self.owner).order_by("pk")

    def get(self, *args, **kwargs) -> JsonResponse:
        cache_key = "user_orders"
        user_orders_data = cache.get(cache_key)
        if user_orders_data is None:
            user_orders_data = [
                OrderSerializer(self.get_queryset(), many=True).data
            ]
            cache.set(cache_key, user_orders_data, 60 * 3)
        return JsonResponse({"user_orders": user_orders_data})
