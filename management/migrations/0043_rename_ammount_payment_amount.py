# Generated by Django 4.1 on 2023-06-17 11:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0042_sampleformverifier_created_date_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='payment',
            old_name='ammount',
            new_name='amount',
        ),
    ]
