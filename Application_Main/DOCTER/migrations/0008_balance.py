# Generated by Django 4.1.5 on 2023-01-28 06:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('PATIENT', '0014_alter_patient_blood'),
        ('DOCTER', '0007_amount_patient_amount_transac_id_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Balance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('balance_amt', models.IntegerField(blank=True, null=True)),
                ('previous_deal_date', models.DateTimeField(auto_now=True)),
                ('patient', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='PATIENT.patient')),
            ],
        ),
    ]
