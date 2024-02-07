# Generated by Django 4.1 on 2023-05-29 08:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0019_remove_sampleform_commodity_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='sampleform',
            name='commodity_id',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='sample_form', to='management.commodity'),
        ),
    ]