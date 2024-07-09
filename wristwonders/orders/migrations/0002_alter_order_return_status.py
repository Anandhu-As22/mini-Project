# Generated by Django 5.0.6 on 2024-07-08 03:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='return_status',
            field=models.CharField(choices=[('none', 'none'), ('Return Requested', 'Return Requested'), ('Returned', 'Returned'), ('Rejected', 'Rejected')], default='none', max_length=100),
        ),
    ]