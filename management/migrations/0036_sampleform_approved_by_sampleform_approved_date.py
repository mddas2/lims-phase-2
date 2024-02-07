# Generated by Django 4.1 on 2023-06-13 05:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('management', '0035_alter_sampleform_amendments_alter_sampleform_note_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='sampleform',
            name='approved_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sample_form_approve', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='sampleform',
            name='approved_date',
            field=models.DateField(null=True),
        ),
    ]