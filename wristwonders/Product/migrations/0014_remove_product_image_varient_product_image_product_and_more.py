# Generated by Django 5.0.6 on 2024-08-20 05:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Product', '0013_remove_product_image_product_product_image_varient'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product_image',
            name='varient',
        ),
        migrations.AddField(
            model_name='product_image',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='images', to='Product.product'),
        ),
        migrations.AlterField(
            model_name='product',
            name='Product_name',
            field=models.CharField(max_length=300, unique=True),
        ),
        migrations.DeleteModel(
            name='ProductVarient',
        ),
    ]
