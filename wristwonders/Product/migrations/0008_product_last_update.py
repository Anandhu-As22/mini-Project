# Generated by Django 5.0.6 on 2024-08-13 05:10

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Product', '0007_category_offer_productoffer'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='last_update',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
