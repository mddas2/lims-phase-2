# Generated by Django 4.1 on 2023-07-01 08:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0023_alter_customuser_phone'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='test_type',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
