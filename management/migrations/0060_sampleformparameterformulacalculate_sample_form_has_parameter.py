# Generated by Django 4.1 on 2023-06-23 12:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0059_remove_sampleformparameterformulacalculate_sample_form_has_parameter'),
    ]

    operations = [
        migrations.AddField(
            model_name='sampleformparameterformulacalculate',
            name='sample_form_has_parameter',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='formula_calculate', to='management.sampleformhasparameter'),
        ),
    ]
