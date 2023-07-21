from django.core.management import BaseCommand

from blogapp.models import Category


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write("Create category")
        category, created = Category.objects.get_or_create(
            name="smartphones",
        )
        category.save()

        self.stdout.write(f"Created category {category.name}")
