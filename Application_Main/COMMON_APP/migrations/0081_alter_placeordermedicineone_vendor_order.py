# Generated by Django 3.2.5 on 2023-10-06 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('COMMON_APP', '0080_alter_placeordermedicineone_vendor_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='placeordermedicineone',
            name='vendor_order',
            field=models.ManyToManyField(to='COMMON_APP.AddVendorStock'),
        ),
    ]
