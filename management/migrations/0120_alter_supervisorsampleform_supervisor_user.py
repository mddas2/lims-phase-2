# Generated by Django 4.1 on 2023-07-19 06:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('management', '0119_sampleform_admin_remarks_sampleform_verifier_remarks'),
    ]

    operations = [
        migrations.AlterField(
            model_name='supervisorsampleform',
            name='supervisor_user',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='supervisor_sample_form', to=settings.AUTH_USER_MODEL),
        ),
    ]
