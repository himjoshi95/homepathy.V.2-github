# Generated by Django 4.1.5 on 2023-01-19 08:10

from django.db import migrations, models
import django.db.models.deletion
import jsignature.fields


class Migration(migrations.Migration):

    dependencies = [
        ('PATIENT', '0010_alter_imagesupload_date'),
        ('DOCTER', '0002_contents_gnm_sbs_item_jsignaturemodel_quote_sign_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExampleModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('signature', jsignature.fields.JSignatureField(blank=True, null=True, verbose_name='Signature')),
                ('signature_date', models.DateTimeField(blank=True, null=True, verbose_name='Signature date')),
                ('patient', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='PATIENT.patient')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
