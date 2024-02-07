# Generated by Django 4.1 on 2023-05-29 06:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('management', '0007_remove_sampleform_supervisor_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='sampleform',
            name='supervisor_user',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sample_has_parameters', to=settings.AUTH_USER_MODEL),
        ),
    ]