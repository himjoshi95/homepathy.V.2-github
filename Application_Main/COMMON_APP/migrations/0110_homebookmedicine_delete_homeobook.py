# Generated by Django 4.2.3 on 2023-11-03 06:46

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("COMMON_APP", "0109_placeorderdoctor_email_status"),
    ]

    operations = [
        migrations.CreateModel(
            name="HomeBookMedicine",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("description", ckeditor.fields.RichTextField()),
                ("created_date", models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.DeleteModel(
            name="HomeoBook",
        ),
    ]
