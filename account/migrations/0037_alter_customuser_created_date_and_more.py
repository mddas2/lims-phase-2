# Generated by Django 4.1 on 2023-11-05 08:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0036_alter_customuser_department_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='updated_date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
