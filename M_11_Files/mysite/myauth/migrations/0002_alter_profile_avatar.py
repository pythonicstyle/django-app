# Generated by Django 4.0.6 on 2023-04-20 17:28

from django.db import migrations, models
import myauth.models


class Migration(migrations.Migration):

    dependencies = [
        ('myauth', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to=myauth.models.avatar_preview_directory_path),
        ),
    ]
