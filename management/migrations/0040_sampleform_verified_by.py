# Generated by Django 4.1 on 2023-06-15 06:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('management', '0039_sampleform_completed_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='sampleform',
            name='verified_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sample_form_verified_by', to=settings.AUTH_USER_MODEL),
        ),
    ]
