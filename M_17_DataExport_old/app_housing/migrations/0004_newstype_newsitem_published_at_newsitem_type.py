# Generated by Django 4.2.1 on 2023-06-12 20:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_housing', '0003_remove_newsitem_published_at_remove_newsitem_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='NewsType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('code', models.CharField(max_length=64)),
            ],
        ),
        migrations.AddField(
            model_name='newsitem',
            name='published_at',
            field=models.DateTimeField(null=True, verbose_name='Дата публикации'),
        ),
        migrations.AddField(
            model_name='newsitem',
            name='type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='news', to='app_housing.newsitem'),
        ),
    ]
