# Generated by Django 2.2.14 on 2023-01-10 16:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('WMapp', '0010_remove_order_billing_address'),
    ]

    operations = [
        migrations.RenameField(
            model_name='address',
            old_name='country',
            new_name='city',
        ),
    ]
