# Generated by Django 4.1 on 2023-07-11 07:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0095_payment_owner_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sampleform',
            name='report_date',
            field=models.DateField(null=True),
        ),
    ]