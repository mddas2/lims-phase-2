# Generated by Django 4.1 on 2023-05-30 09:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0021_rename_commodity_id_sampleform_commodity'),
    ]

    operations = [
        migrations.AddField(
            model_name='sampleformparameterformulacalculate',
            name='is_verified',
            field=models.BooleanField(default=False),
        ),
    ]
