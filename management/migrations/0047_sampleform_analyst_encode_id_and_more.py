# Generated by Django 4.1 on 2023-06-18 18:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0046_sampleform_requested_export'),
    ]

    operations = [
        migrations.AddField(
            model_name='sampleform',
            name='analyst_encode_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='sampleform',
            name='supervisor_encode_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='sampleform',
            name='user_encode_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='sampleform',
            name='verifier_encode_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
