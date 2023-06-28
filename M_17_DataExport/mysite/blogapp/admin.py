from django.contrib import admin

from .models import Article, Category, Tag


class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'pub_data']


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']


class TagAdmin(admin.ModelAdmin):
    list_display = ['name']


admin.site.register(Article, ArticleAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)

