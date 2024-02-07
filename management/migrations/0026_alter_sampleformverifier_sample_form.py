# Generated by Django 4.1 on 2023-06-01 08:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0025_alter_sampleform_parameters_sampleformverifier'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sampleformverifier',
            name='sample_form',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='verifier', to='management.sampleform'),
        ),
    ]