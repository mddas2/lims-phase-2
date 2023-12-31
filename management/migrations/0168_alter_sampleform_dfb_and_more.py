# Generated by Django 4.1 on 2023-09-10 10:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0167_alter_rawdatasheet_sample_received_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sampleform',
            name='dfb',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='supervisorsampleform',
            name='status',
            field=models.CharField(blank=True, choices=[('pending', 'pending'), ('not_assigned', 'not_assigned'), ('processing', 'processing'), ('completed', 'completed'), ('recheck', 'recheck'), ('rejected', 'rejected'), ('not_verified', 'not_verified'), ('not_approved', 'not_approved'), ('Test Completed', 'Test Completed'), ('verified', 'verified')], default='not_assigned', max_length=155, null=True),
        ),
    ]
