# Generated by Django 4.2.1 on 2023-06-12 20:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_housing', '0004_newstype_newsitem_published_at_newsitem_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='newsitem',
            name='published_at',
        ),
    ]
