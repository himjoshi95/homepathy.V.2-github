# Generated by Django 4.1.5 on 2023-02-02 06:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DOCTER', '0009_amount_balance_flag'),
    ]

    operations = [
        migrations.AddField(
            model_name='amount',
            name='cash_amount',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='amount',
            name='online_amount',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
