# Generated by Django 4.1 on 2023-06-20 06:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('websocket', '0003_notification_created_date_notification_updated_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='isinstance_id',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
