# Generated by Django 4.2.3 on 2023-08-25 15:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('COMMON_APP', '0040_appointment_email_flag'),
    ]

    operations = [
        migrations.AddField(
            model_name='hr',
            name='forget_password_token',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='receptionist',
            name='forget_password_token',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
