# Generated by Django 4.2.1 on 2023-05-12 20:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myauth', '0002_alter_profile_avatar'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='profile',
            options={'verbose_name': 'profile', 'verbose_name_plural': 'profiles'},
        ),
    ]
