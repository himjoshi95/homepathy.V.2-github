# Generated by Django 3.2.5 on 2023-10-10 08:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('COMMON_APP', '0084_medicinestocklist_order_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='placeordermedicineone',
            name='pack',
            field=models.CharField(choices=[('', 'Please Select'), ('10 ML', '10 ML'), ('30 ML', '30 ML'), ('100 ML', '100 ML'), ('450 ML', '450 ML')], max_length=100, null=True),
        ),
    ]
