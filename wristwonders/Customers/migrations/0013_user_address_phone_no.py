# Generated by Django 5.0.6 on 2024-06-28 05:28

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Customers', '0012_alter_cart_items_quantity'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_address',
            name='phone_no',
            field=models.CharField(default=1234567890, max_length=10, validators=[django.core.validators.RegexValidator(message='phone number must be 10 digits long', regex='^\\d{10}$')]),
        ),
    ]