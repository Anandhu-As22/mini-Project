# Generated by Django 5.0.6 on 2024-06-28 10:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Customers', '0017_rename_street_user_address_house_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_address',
            name='street',
            field=models.CharField(default='deffault', max_length=255),
            preserve_default=False,
        ),
    ]