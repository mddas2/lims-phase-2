# Generated by Django 4.1 on 2023-11-06 06:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('management', '0179_sampleform_created_by_user_sampleform_owner_user_obj'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sampleform',
            name='owner_user_obj',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='suser_have_sample_form', to=settings.AUTH_USER_MODEL),
        ),
    ]
