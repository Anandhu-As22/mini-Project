# Generated by Django 5.0.6 on 2024-06-16 12:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Product', '0003_remove_product_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product_image',
            name='image',
            field=models.FileField(upload_to='images'),
        ),
    ]
