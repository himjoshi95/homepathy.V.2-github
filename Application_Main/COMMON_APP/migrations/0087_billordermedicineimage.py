# Generated by Django 3.2.5 on 2023-10-10 16:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('COMMON_APP', '0086_ordermedicineitem_is_verified'),
    ]

    operations = [
        migrations.CreateModel(
            name='BillOrderMedicineImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bill_images', models.ImageField(upload_to='images')),
                ('bill_image_timestamp', models.DateField(auto_now_add=True)),
                ('ordered_med', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='COMMON_APP.ordermedicineitem')),
            ],
        ),
    ]
