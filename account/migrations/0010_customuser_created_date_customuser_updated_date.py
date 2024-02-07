# Generated by Django 4.1 on 2023-06-13 07:58

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0009_alter_customuser_approved_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='created_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='customuser',
            name='updated_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]