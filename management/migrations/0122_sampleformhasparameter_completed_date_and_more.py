# Generated by Django 4.1 on 2023-07-20 07:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0121_alter_sampleformhasparameter_analyst_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='sampleformhasparameter',
            name='completed_date',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='sampleformhasparameter',
            name='sample_receive_date',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='sampleformhasparameter',
            name='started_date',
            field=models.DateTimeField(null=True),
        ),
    ]
