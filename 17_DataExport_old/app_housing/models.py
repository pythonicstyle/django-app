from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class RoomCount(models.Model):
    """
    Модель RoomCount представляет количество комнат в жилье
    """

    count = models.PositiveIntegerField(db_index=True)
    description = models.TextField(blank=True, max_length=128)

    def __str__(self):
        return self.description


class Type(models.Model):
    """
    Модель Type представляет тип помещения
    """

    name = models.CharField(max_length=128, db_index=True)

    def __str__(self):
        return self.name


class Housing(models.Model):
    """
    Модель Housing представляет жильё
    """

    name = models.CharField(max_length=200, db_index=True)
    description = models.TextField(null=False, blank=True)
    pub_data = models.DateTimeField(auto_now_add=True)
    agent = models.ForeignKey(User, on_delete=models.CASCADE, default="anonymous user")
    type = models.ForeignKey(Type, on_delete=models.CASCADE, blank=True, related_name="type")
    room_area = models.PositiveIntegerField(default=0)
    rooms = models.ForeignKey(RoomCount, on_delete=models.CASCADE, related_name="rooms")
    price = models.PositiveIntegerField(default=0)
    is_published = models.BooleanField(default=False)


class NewsItem(models.Model):
    """
    Модель NewsItem представляет новости
    """

    title = models.CharField(max_length=128, db_index=True, verbose_name="Заголовок")
    description = models.TextField(verbose_name="Текст статьи")
    is_published = models.BooleanField(default=False)
    type = models.ForeignKey('NewsItem', on_delete=models.CASCADE, null=True, related_name="news")
    published_at = models.DateTimeField(null=True, verbose_name="Дата публикации")

    def get_absolute_url(self):
        return reverse("news-item", args=[str(self.pk)])

    def __str__(self):
        return self.title


class NewsType(models.Model):
    """
    Модель NewsType представляет тип новости
    """

    name = models.CharField(max_length=128)
    code = models.CharField(max_length=64)

    def __str__(self):
        return self.name
