# Generated by Django 4.1 on 2023-06-13 11:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0036_sampleform_approved_by_sampleform_approved_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sampleformparameterformulacalculate',
            name='result',
            field=models.FloatField(null=True),
        ),
    ]
