# Generated by Django 4.2.1 on 2023-06-03 14:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blogapp', '0002_alter_article_category'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='article',
            options={'ordering': ['title', 'pub_data'], 'verbose_name': 'article', 'verbose_name_plural': 'articles'},
        ),
    ]
