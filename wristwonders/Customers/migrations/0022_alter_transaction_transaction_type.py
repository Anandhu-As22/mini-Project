# Generated by Django 5.0.6 on 2024-08-01 05:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Customers', '0021_transaction'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='transaction_type',
            field=models.CharField(choices=[('debit', 'Debit'), ('Credit', 'credit'), ('refund', 'Refund')], max_length=10),
        ),
    ]