# Generated by Django 4.2.3 on 2023-11-27 19:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("DOCTER", "0026_remove_balance_bal_date_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="balance",
            name="previous_deal_date",
            field=models.DateField(auto_now_add=True),
        ),
    ]
