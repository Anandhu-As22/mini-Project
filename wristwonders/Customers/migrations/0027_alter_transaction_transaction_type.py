# Generated by Django 5.0.6 on 2024-08-19 10:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Customers', '0026_alter_transaction_transaction_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='transaction_type',
            field=models.CharField(choices=[('debit', 'Debit'), ('refund', 'Refund'), ('Credit', 'credit')], max_length=10),
        ),
    ]
