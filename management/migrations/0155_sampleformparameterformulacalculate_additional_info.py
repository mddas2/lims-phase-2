# Generated by Django 4.1 on 2023-08-10 12:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0154_rawdatasheetdetail_micro_table'),
    ]

    operations = [
        migrations.AddField(
            model_name='sampleformparameterformulacalculate',
            name='additional_info',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
