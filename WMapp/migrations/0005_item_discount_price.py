# Generated by Django 2.2.14 on 2023-01-06 00:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WMapp', '0004_item_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='discount_price',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
