# Generated by Django 3.2.12 on 2024-06-24 19:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database_handling_app', '0005_auto_20240625_0124'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='year',
            field=models.CharField(default='Data Not Available', max_length=5),
        ),
    ]
