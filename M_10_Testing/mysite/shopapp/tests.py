from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.conf import settings

from shopapp.models import Product, Order


class ProductCreateViewTestCase(TestCase):

    def test_create_product(self):
        response = self.client.post(
            reverse("shopapp:product_create"),
            {
                "name": "Table",
                "price": "123.43",
                "description": "grgw",
                "discount": "12",
                "created_by": "user"
            }
        )
        self.assertRedirects(response, reverse("shopapp:products_list"))


class ProductDetailViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):  # создает объект, чтобы убедиться, что он был создан имеено при тестировании,
        # выполняет предварительную настройку
        cls.product = Product.objects.create(name="Best Product")

    @classmethod
    def tearDownClass(cls):  # удаляет созданный перед тестом объект
        cls.product.delete()

    def test_get_product(self):  # проверяет получение страницы и сверяет статус код
        response = self.client.get(
            reverse("shopapp:product_details", kwargs={"pk": self.product.pk})
        )
        self.assertEqual(response.status_code, 200)

    def test_get_product_and_check_content(self):  # проверяет полученную страницу на содержание имени продукта
        response = self.client.get(
            reverse("shopapp:product_details", kwargs={"pk": self.product.pk})
        )
        self.assertContains(response, self.product.name)
        # для обоих тестов сущность продуктов создана только один раз
        # перед началом выполнения всех тестов внутри класса


class ProductListViewTestCase(TestCase):
    fixtures = [
        'products-fixtures.json',
    ]

    def test_product(self):
        response = self.client.get(reverse("shopapp:products_list"))
        # products = Product.objects.filter(archived=False).all()
        # products_ = response.context["products"]
        self.assertQuerysetEqual(
            qs=Product.objects.filter(archived=False).all(),
            values=(p.pk for p in response.context["products"]),
            transform=lambda p: p.pk,
        )

        self.assertTemplateUsed(response, 'shopapp/products-list.html')


class OrdersListViewTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.user = User.objects.create_user(username="bob_test", password="1234")

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()

    def setUp(self) -> None:
        self.client.force_login(self.user)

    def test_orders_view(self):
        response = self.client.get(reverse("shopapp:orders_list"))
        self.assertContains(response, "Orders")

    def test_orders_view_not_authenticated(self):
        self.client.logout()
        response = self.client.get(reverse("shopapp:orders_list"))
        # self.assertRedirects(response, str(settings.LOGIN_URL))
        self.assertEqual(response.status_code, 302)
        self.assertIn(str(settings.LOGIN_URL), response.url)


class ProductsExportViewTestCase(TestCase):
    fixtures = [
        'products-fixtures.json'
    ]

    def test_get_products_view(self):
        response = self.client.get(
            reverse("shopapp:products-export"),
        )
        self.assertEqual(response.status_code, 200)
        products = Product.objects.order_by("pk").all()
        expected_data = [
            {
                "pk": product.pk,
                "name": product.name,
                "price": str(product.price),
                "archived": product.archived,
                "created by": product.created_by,
            }
            for product in products
        ]
        products_data = response.json()
        self.assertEqual(
            products_data["products"],
            expected_data
        )


class OrderDetailViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.user = User.objects.with_perm(perm="shopapp.view_order")

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()

    def setUp(self) -> None:
        self.client.force_login(self.user)

    def tearDown(self) -> None:
        self.client.delete()

    def test_order_details(self):
        response = self.client.get(reverse("shopapp:order_details"))
        self.assertContains(response, "delivery_address")
        self.assertContains(response, "promocode")
