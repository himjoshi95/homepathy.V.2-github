# Generated by Django 4.1.6 on 2023-07-13 10:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('PATIENT', '0017_newcasepaperupload'),
        ('dashboard', '0029_familymedicalcomplain'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='PastHistoryNew',
            new_name='PresentComplaintsNew',
        ),
    ]
