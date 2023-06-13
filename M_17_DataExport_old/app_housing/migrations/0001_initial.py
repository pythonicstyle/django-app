# Generated by Django 4.2.1 on 2023-06-12 09:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='RoomCount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField(db_index=True)),
                ('description', models.TextField(blank=True, max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='Type',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='NewsItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(db_index=True, max_length=128, verbose_name='Заголовок')),
                ('description', models.TextField(verbose_name='Текст статьи')),
                ('is_published', models.BooleanField(default=False)),
                ('published_at', models.DateTimeField(null=True, verbose_name='Дата публикации')),
                ('type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='news', to='app_housing.newsitem')),
            ],
        ),
        migrations.CreateModel(
            name='Housing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=200)),
                ('description', models.TextField(blank=True)),
                ('pub_data', models.DateTimeField(auto_now_add=True)),
                ('is_published', models.BooleanField(default=False)),
                ('agent', models.ForeignKey(default='anonymous user', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('rooms', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rooms', to='app_housing.roomcount')),
                ('type', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='type', to='app_housing.type')),
            ],
        ),
    ]
