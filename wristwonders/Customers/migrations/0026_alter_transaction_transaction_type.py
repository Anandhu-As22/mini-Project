# Generated by Django 5.0.6 on 2024-08-14 04:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Customers', '0025_alter_transaction_transaction_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='transaction_type',
            field=models.CharField(choices=[('debit', 'Debit'), ('Credit', 'credit'), ('refund', 'Refund')], max_length=10),
        ),
    ]