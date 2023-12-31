# Generated by Django 4.1 on 2023-06-21 12:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0020_alter_customuser_department_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='department_address',
            field=models.CharField(choices=[('f', 'Kathmandu'), ('fk', 'Ktm'), ('fdh', 'Dhulikhel'), ('fsur', 'Surkhet'), ('ftha', 'Tanahun'), ('fp', 'Pokhara'), ('fex', 'Other'), ('fnu', 'Nuwakot'), ('fsin', 'Sindhuli'), ('null', 'N/A')], default=None, max_length=60, null=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='registration_document',
            field=models.FileField(default=None, upload_to='media/user/registration'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='renew_document',
            field=models.FileField(default=None, upload_to='media/user/renew_doument'),
        ),
    ]
