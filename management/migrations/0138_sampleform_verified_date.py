# Generated by Django 4.1 on 2023-08-02 06:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0137_rawdatasheetdetail_mandatory_standard_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='sampleform',
            name='verified_date',
            field=models.DateTimeField(null=True),
        ),
    ]