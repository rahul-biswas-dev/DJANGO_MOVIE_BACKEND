# Generated by Django 3.2.12 on 2024-07-01 12:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database_handling_app', '0006_alter_movie_year'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='backdrop_url',
            field=models.URLField(blank=True, max_length=455, null=True),
        ),
    ]
