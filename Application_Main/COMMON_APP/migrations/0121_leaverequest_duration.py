# Generated by Django 4.2.3 on 2023-11-08 11:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("COMMON_APP", "0120_remove_leaverequest_approved_by"),
    ]

    operations = [
        migrations.AddField(
            model_name="leaverequest",
            name="duration",
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
