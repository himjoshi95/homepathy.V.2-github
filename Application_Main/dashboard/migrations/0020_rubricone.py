# Generated by Django 4.1.5 on 2023-03-08 18:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('PATIENT', '0015_patient_display_flag'),
        ('dashboard', '0019_miasmone'),
    ]

    operations = [
        migrations.CreateModel(
            name='RubricOne',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rubric', models.CharField(blank=True, max_length=50, null=True)),
                ('date', models.DateField(auto_now=True)),
                ('patient', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='PATIENT.patient')),
            ],
        ),
    ]
