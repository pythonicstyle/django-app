from django.contrib.auth.models import User
from django.core.management import BaseCommand

from blogapp.models import Author


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write("Create author")
        user = User.objects.get(username="admin1")
        author, created = Author.objects.get_or_create(
            name=user,
        )

        self.stdout.write(f"Author {author.name} created")
