# Generated by Django 5.0.6 on 2024-08-14 04:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Product', '0008_product_last_update'),
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
        ),
    ]
