# Generated by Django 4.1 on 2023-08-09 10:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0146_alter_microobservationtablerawdata_micro_parameter_table_raw_data'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='microparameterrawdata',
            name='sample_form_has_parameter',
        ),
    ]
