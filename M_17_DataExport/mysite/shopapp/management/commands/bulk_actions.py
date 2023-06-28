from django.contrib.auth.models import User
from django.core.management import BaseCommand

from shopapp.models import Order, Product


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write("Start demo bulk actions")

        #  обновление сразу нескольких объектов за один запрос к БД
        result = Product.objects.filter(
            name__contains="Smartphone",
        ).update(discount=10)

        print(result)

        #  создание сразу нескольких продуктов
        # info = [
        #     ("Smartphone 12", 299),
        #     ("Smartphone 13", 399),
        #     ("Smartphone 14", 499),
        # ]
        # products = [
        #     Product(name=name, price=price)
        #     for name, price in info
        # ]
        #
        # result = Product.objects.bulk_create(products)
        #
        # for obj in result:
        #     print(obj)

        self.stdout.write("Done")
