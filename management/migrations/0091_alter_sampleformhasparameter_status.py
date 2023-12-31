# Generated by Django 4.1 on 2023-07-03 03:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0090_merge_20230703_0207'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sampleformhasparameter',
            name='status',
            field=models.CharField(blank=True, choices=[('pending', 'pending'), ('processing', 'processing'), ('completed', 'completed'), ('recheck', 'recheck'), ('rejected', 'rejected'), ('not_verified', 'not_verified'), ('tested', 'tested'), ('verified', 'verified')], default='pending', max_length=155, null=True),
        ),
    ]
