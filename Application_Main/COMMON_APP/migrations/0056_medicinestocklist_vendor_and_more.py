# Generated by Django 4.2.4 on 2023-09-08 20:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('COMMON_APP', '0055_vendormedicine'),
    ]

    operations = [
        migrations.AddField(
            model_name='medicinestocklist',
            name='vendor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='COMMON_APP.addvendorstock'),
        ),
        migrations.AlterField(
            model_name='medicinestocklist',
            name='medicine',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='COMMON_APP.vendormedicine'),
        ),
    ]
