# Generated by Django 4.2.4 on 2023-09-08 15:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('COMMON_APP', '0052_stock_vendor_alter_stock_stock_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='PlaceOrderStock',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_quantity', models.IntegerField()),
                ('unit', models.CharField(choices=[('', 'Please Select Unit from list'), ('Kg', 'Kg'), ('Piece', 'Piece'), ('Packet', 'Packet'), ('Bottle', 'Bottle'), ('Box', 'Box')], max_length=50, null=True)),
                ('order_timestamp', models.DateTimeField(auto_now_add=True)),
                ('order_delivery_date', models.DateField()),
                ('email', models.EmailField(max_length=254)),
                ('stock_order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='COMMON_APP.stock')),
            ],
        ),
    ]
