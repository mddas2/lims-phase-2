# Generated by Django 4.1 on 2023-08-03 06:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0138_sampleform_verified_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='microparameter',
            name='first_exponent',
            field=models.CharField(default=None, max_length=500),
        ),
        migrations.AddField(
            model_name='microparameter',
            name='second_exponent',
            field=models.CharField(default=None, max_length=500),
        ),
        migrations.AddField(
            model_name='microparameter',
            name='third_exponent',
            field=models.CharField(default=None, max_length=500),
        ),
    ]
