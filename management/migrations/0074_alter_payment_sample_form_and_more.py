# Generated by Django 4.1 on 2023-06-28 11:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0073_alter_commodity_test_duration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='sample_form',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='payment', to='management.sampleform'),
        ),
        migrations.AlterField(
            model_name='sampleformhasparameter',
            name='status',
            field=models.CharField(blank=True, choices=[('pending', 'pending'), ('processing', 'processing'), ('completed', 'completed'), ('recheck', 'recheck'), ('rejected', 'rejected'), ('not_verified', 'not_verified'), ('verified', 'verified')], default='pending', max_length=155, null=True),
        ),
        migrations.AlterField(
            model_name='sampleformparameterformulacalculate',
            name='status',
            field=models.CharField(choices=[('pending', 'pending'), ('rejected', 'rejected'), ('recheck', 'recheck'), ('completed', 'completed'), ('processing', 'processing')], default='processing', max_length=155),
        ),
    ]
