# Generated by Django 4.1 on 2023-10-01 10:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0172_microparameter_time_of_incubation_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='microparameterrawdata',
            name='date_of_incubation',
            field=models.CharField(max_length=500, null=True),
        ),
    ]