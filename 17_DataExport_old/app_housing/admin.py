from django.contrib import admin
from .models import RoomCount, Type, Housing, NewsItem, NewsType


class HousingAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'agent', 'price']


class TypeAdmin(admin.ModelAdmin):
    list_display = ['name']


class RoomCountAdmin(admin.ModelAdmin):
    list_display = ['count', 'description']


class NewsItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'title']


class NewsTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'code']


admin.site.register(Housing, HousingAdmin)
admin.site.register(Type, TypeAdmin)
admin.site.register(RoomCount, RoomCountAdmin)
admin.site.register(NewsItem, NewsItemAdmin)
admin.site.register(NewsType, NewsTypeAdmin)
