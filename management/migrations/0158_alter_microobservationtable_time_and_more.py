# Generated by Django 4.1 on 2023-08-16 06:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0157_sampleform_analysis_fee_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='microobservationtable',
            name='time',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='microobservationtablerawdata',
            name='time',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
