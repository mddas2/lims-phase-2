# Generated by Django 4.1 on 2023-06-07 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0030_rename_is_tested_sampleformhasparameter_is_supervisor_sent'),
    ]

    operations = [
        migrations.AddField(
            model_name='sampleform',
            name='is_analyst_test',
            field=models.BooleanField(default=False),
        ),
    ]
