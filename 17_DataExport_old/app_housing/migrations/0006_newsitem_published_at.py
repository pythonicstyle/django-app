# Generated by Django 4.2.1 on 2023-06-12 20:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_housing', '0005_remove_newsitem_published_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='newsitem',
            name='published_at',
            field=models.DateTimeField(null=True, verbose_name='Дата публикации'),
        ),
    ]