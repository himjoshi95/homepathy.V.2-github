# Generated by Django 3.2.5 on 2023-09-23 18:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('COMMON_APP', '0065_placeordermedicine_order_received_flag'),
    ]

    operations = [
        migrations.AddField(
            model_name='placeordermedicine',
            name='potency',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='COMMON_APP.addpotencyhr'),
        ),
    ]
