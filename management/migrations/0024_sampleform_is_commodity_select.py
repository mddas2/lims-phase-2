# Generated by Django 4.1 on 2023-05-31 06:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0023_alter_sampleformhasparameter_status_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='sampleform',
            name='is_commodity_select',
            field=models.BooleanField(default=False),
        ),
    ]
