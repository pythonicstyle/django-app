# Generated by Django 4.1.7 on 2023-04-10 18:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shopapp', '0007_alter_order_options_alter_product_options_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='created_by',
        ),
    ]
