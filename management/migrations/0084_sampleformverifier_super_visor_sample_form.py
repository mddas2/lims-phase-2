# Generated by Django 4.1 on 2023-07-01 20:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0083_alter_sampleformhasparameter_commodity'),
    ]

    operations = [
        migrations.AddField(
            model_name='sampleformverifier',
            name='super_visor_sample_form',
            field=models.ManyToManyField(null=True, related_name='verifiers', to='management.supervisorsampleform'),
        ),
    ]