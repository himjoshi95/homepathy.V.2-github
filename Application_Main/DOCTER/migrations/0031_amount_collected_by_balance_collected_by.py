# Generated by Django 4.2.3 on 2023-12-05 11:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("DOCTER", "0030_alter_balance_previous_deal_date"),
    ]

    operations = [
        migrations.AddField(
            model_name="amount",
            name="collected_by",
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="balance",
            name="collected_by",
            field=models.CharField(max_length=255, null=True),
        ),
    ]
