# Generated by Django 3.2.12 on 2024-07-08 16:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database_handling_app', '0007_movie_backdrop_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='logo_url',
            field=models.URLField(blank=True, max_length=455, null=True),
        ),
    ]
