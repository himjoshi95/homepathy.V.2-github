# Generated by Django 3.2.5 on 2023-09-30 09:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('COMMON_APP', '0073_auto_20230929_2026'),
    ]

    operations = [
        migrations.CreateModel(
            name='PlaceOrderMedicineOne',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_quantity', models.IntegerField()),
                ('medicine_order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='COMMON_APP.medicinestocklist')),
                ('potency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='COMMON_APP.addpotencyhr')),
                ('vendor_order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='COMMON_APP.addvendorstock')),
            ],
        ),
    ]
