from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User, Permission
from django.conf import settings

from shopapp.models import Product, Order


class ProductCreateViewTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.credentials = dict(username='1', password='1111', is_superuser=True)
        cls.user = User.objects.create_user(**cls.credentials)

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()

    def setUp(self):
        self.client.login(**self.credentials)

    def test_create_product(self):
        response = self.client.post(reverse("shopapp:product_create"))
        self.assertEqual(response.status_code, 200)
        # self.assertRedirects(response, reverse("shopapp:products_list"))


class ProductDetailViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.product = Product.objects.create(name="Best Product")

    @classmethod
    def tearDownClass(cls):
        cls.product.delete()

    def test_get_product(self):
        response = self.client.get(
            reverse("shopapp:product_details", kwargs={"pk": self.product.pk})
        )
        self.assertEqual(response.status_code, 200)

    def test_get_product_and_check_content(self):
        response = self.client.get(
            reverse("shopapp:product_details", kwargs={"pk": self.product.pk})
        )
        self.assertContains(response, self.product.name)


class ProductListViewTestCase(TestCase):
    fixtures = [
        'users-fixtures.json',
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
        'users-fixtures.json',
        'products-fixtures.json',
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
                "created by": product.created_by_id,
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
        cls.credentials = dict(username='admin1', password='1111', is_superuser=True)
        cls.user = User.objects.create_user(**cls.credentials)
        cls.user.user_permissions.add(Permission.objects.get(codename="view_order"))

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()

    def setUp(self) -> None:
        self.client.force_login(self.user)
        self.order = Order.objects.create(
            pk="1",
            delivery_address="Moscow",
            promocode="SALE50",
            user=self.user,
        )

    def tearDown(self) -> None:
        self.order.delete()

    def test_order_details(self):
        response = self.client.get(reverse('shopapp:order_details', kwargs={'pk': self.order.pk}))
        self.assertContains(response, self.order.delivery_address)
        self.assertContains(response, self.order.promocode)
        order_data = response.context["order"]
        self.assertEqual(order_data.pk, self.order.pk)


class OrdersExportTestCase(TestCase):
    fixtures = [
        'users-fixtures.json',
        'products-fixtures.json',
        'orders-fixtures.json',
    ]

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.credentials = dict(username='admin_test', password='1111', is_staff=True)
        cls.user = User.objects.create_user(**cls.credentials)
        cls.user.user_permissions.add(Permission.objects.get(codename="view_order"))

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()

    def setUp(self):
        self.client.login(**self.credentials)

    def test_get_products_view(self):
        response = self.client.get(reverse('shopapp:orders-export'))
        self.assertEqual(response.status_code, 200)
        orders = Order.objects.order_by('pk').all()
        expected_data = [
            {
                "pk": order.pk,
                "delivery_address": order.delivery_address,
                "promocode": order.promocode,
                "user": order.user_id,
                "products": [product.pk for product in order.products.all()],
            }
            for order in orders]
        orders_data = response.json()
        self.assertEqual(orders_data['orders'], expected_data)
