from rest_framework import serializers

from .models import Article


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = (
            "pk",
            "title",
            "content",
            "pub_data",
            "author",
            "category",
            "tags",
        )
