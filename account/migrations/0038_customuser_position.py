# Generated by Django 4.1 on 2023-12-13 11:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0037_alter_customuser_created_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='position',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
