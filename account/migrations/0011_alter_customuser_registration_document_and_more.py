# Generated by Django 4.1 on 2023-06-16 06:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0010_customuser_created_date_customuser_updated_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='registration_document',
            field=models.FileField(null=True, upload_to='media/user/registration'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='renew_document',
            field=models.FileField(null=True, upload_to='media/user/renew_doument'),
        ),
    ]
