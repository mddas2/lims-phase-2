# Generated by Django 4.1 on 2023-06-22 10:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0021_alter_customuser_department_address_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='phone',
            field=models.CharField(default=None, max_length=15, unique=True),
        ),
    ]
