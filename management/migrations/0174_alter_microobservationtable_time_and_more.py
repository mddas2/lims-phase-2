# Generated by Django 4.1 on 2023-10-06 03:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0173_alter_microparameterrawdata_date_of_incubation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='microobservationtable',
            name='time',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='microobservationtablerawdata',
            name='time',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]