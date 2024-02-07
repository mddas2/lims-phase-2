# Generated by Django 4.1 on 2023-05-29 06:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('management', '0009_alter_sampleformhasparameter_analyst_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sampleformhasparameter',
            name='analyst_user',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
