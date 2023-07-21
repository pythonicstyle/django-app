from typing import Sequence
from django.db import transaction
from django.contrib.auth.models import User
from django.core.management import BaseCommand

from shopapp.models import Order, Product


class Command(BaseCommand):
    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write("Create order")
        user = User.objects.get(username="admin1")
        products: Sequence[Product] = Product.objects.defer("description", "created_at").all()
        order, created = Order.objects.get_or_create(
            delivery_address="Wall street",
            promocode="SALE1",
            user=user,
        )
        for product in products:
            order.products.add(product)
        order.save()

        self.stdout.write(f"Created order {order}")
