from django.contrib.auth.models import User
from django.core.management import BaseCommand
from django.db import transaction

from blogapp.models import Article, Category


class Command(BaseCommand):
    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write("Creating article")
        author = User.objects.get(username="admin1")
        category = Category.objects.get(name="smartphones")
        article, created = Article.objects.get_or_create(
            title="some info about smartphone",
            category=category,
            author=author,
        )
        article.save()
        self.stdout.write(f"Article {article.title} created")
