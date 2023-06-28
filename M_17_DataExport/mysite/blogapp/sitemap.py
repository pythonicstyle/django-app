from django.contrib.sitemaps import Sitemap

from .models import Article


class ArticleSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9

    def items(self):
        return Article.objects.filter(is_published=True).all()

    def lastmod(self, obj: Article):
        return obj.pub_data
