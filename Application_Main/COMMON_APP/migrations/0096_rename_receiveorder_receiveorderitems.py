# Generated by Django 4.2.3 on 2023-10-26 22:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("COMMON_APP", "0095_placedorderitems_receiveorder"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="ReceiveOrder",
            new_name="ReceiveOrderItems",
        ),
    ]
