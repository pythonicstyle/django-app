from django.core.management import BaseCommand

from blogapp.models import Article


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write("Start demo selecting fields")

        articles_info = Article.objects.values_list("title", flat=True)
        print(list(articles_info))

        self.stdout.write("Done")
