# Generated by Django 4.1 on 2023-11-05 08:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('websocket', '0007_rename_isinstance_id_notification_instance_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='notification',
            name='updated_date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]