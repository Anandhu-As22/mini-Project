# Generated by Django 5.0.6 on 2024-09-19 05:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Customers', '0044_alter_transaction_transaction_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='transaction_type',
            field=models.CharField(choices=[('Credit', 'credit'), ('refund', 'Refund'), ('debit', 'Debit')], max_length=10),
        ),
    ]