# Generated by Django 4.1 on 2023-06-13 20:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0037_alter_sampleformparameterformulacalculate_result'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sampleformhasparameter',
            name='status',
            field=models.CharField(blank=True, choices=[('pending', 'pending'), ('processing', 'processing'), ('completed', 'completed')], default='pending', max_length=155, null=True),
        ),
        migrations.AlterField(
            model_name='sampleformparameterformulacalculate',
            name='status',
            field=models.CharField(choices=[('pending', 'pending'), ('completed', 'completed'), ('processing', 'processing')], default='processing', max_length=155),
        ),
    ]
