# Generated by Django 4.1 on 2023-07-01 14:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0081_supervisorsampleform_is_analyst_test_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sampleformhasparameter',
            name='super_visor_sample_form',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sample_has_parameter_analyst', to='management.supervisorsampleform'),
        ),
    ]
