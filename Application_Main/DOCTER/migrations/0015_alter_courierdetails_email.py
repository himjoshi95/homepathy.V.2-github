# Generated by Django 4.1.5 on 2023-02-07 16:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DOCTER', '0014_courierdetails_email_flag'),
    ]

    operations = [
        migrations.AlterField(
            model_name='courierdetails',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
    ]
