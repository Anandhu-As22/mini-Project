# Generated by Django 5.0.6 on 2024-08-24 04:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Customers', '0040_alter_transaction_transaction_type_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='transaction_type',
            field=models.CharField(choices=[('refund', 'Refund'), ('debit', 'Debit'), ('Credit', 'credit')], max_length=10),
        ),
    ]
