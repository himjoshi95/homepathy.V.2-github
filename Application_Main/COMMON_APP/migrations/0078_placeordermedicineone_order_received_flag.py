# Generated by Django 3.2.5 on 2023-10-04 17:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('COMMON_APP', '0077_placeordermedicineone_order_delivery_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='placeordermedicineone',
            name='order_received_flag',
            field=models.BooleanField(default=False),
        ),
    ]
