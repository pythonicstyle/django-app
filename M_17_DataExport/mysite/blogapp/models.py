from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User


class Author(models.Model):
    """
    Модель Author представляет автора статьи
    """

    class Meta:
        verbose_name_plural = _("authors")
        verbose_name = _("author")

    name = models.CharField(max_length=100, db_index=True)
    bio = models.TextField(blank=True)


class Category(models.Model):
    """
    Модель Category представляет категорию статьи
    """

    class Meta:
        verbose_name_plural = _("Categories")
        verbose_name = _("Category")

    name = models.CharField(max_length=40, db_index=True)

    def __str__(self):
        return f"{self.name}"


class Tag(models.Model):
    """
    Модель Tag представляет тэги, которые можно назначить статье
    """

    name = models.CharField(max_length=20, db_index=True)

    def __str__(self):
        return f"{self.name!r}"


class Article(models.Model):
    """
    Модель Article представляет статью
    """

    class Meta:
        verbose_name_plural = _("articles")
        verbose_name = _("article")
        ordering = ['title', 'pub_data']

    title = models.CharField(max_length=200, db_index=True)
    content = models.TextField(null=False, blank=True)
    pub_data = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, related_name="category")
    tags = models.ManyToManyField(Tag, related_name="tags")
    is_published = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse('blogapp:article', kwargs={"pk": self.pk})

    def __str__(self):
        return f"{self.title!r}\n{self.author}"
