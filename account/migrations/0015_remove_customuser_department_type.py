# Generated by Django 4.1 on 2023-06-18 08:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0014_rename_department_address_customuser_department_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='department_type',
        ),
    ]
