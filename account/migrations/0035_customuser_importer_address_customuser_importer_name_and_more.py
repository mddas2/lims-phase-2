# Generated by Django 4.1 on 2023-08-17 05:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0034_alter_customuser_is_email_verified'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='importer_address',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='importer_name',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='other_detail',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
