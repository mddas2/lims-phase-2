# Generated by Django 4.1 on 2023-07-11 12:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0105_microobservationtable'),
    ]

    operations = [
        migrations.AddField(
            model_name='microobservationtable',
            name='micro_parameter_table',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='micro_observation_table', to='management.microparameter'),
        ),
        migrations.AddField(
            model_name='microobservationtable',
            name='parameter',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='management.testresult'),
        ),
        migrations.AddField(
            model_name='microobservationtable',
            name='sample_form',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='micro_observation_table', to='management.sampleform'),
        ),
        migrations.AddField(
            model_name='sampleformparameterformulacalculate',
            name='analyst_remarks',
            field=models.CharField(max_length=200, null=True),
        ),
    ]