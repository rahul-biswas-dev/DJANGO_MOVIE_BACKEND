# Generated by Django 3.2.12 on 2024-07-22 15:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database_handling_app', '0016_auto_20240722_2035'),
    ]

    operations = [
        migrations.AlterField(
            model_name='logos',
            name='iso_639_1',
            field=models.CharField(default='en', max_length=10),
        ),
    ]
