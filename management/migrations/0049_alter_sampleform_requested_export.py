# Generated by Django 4.1 on 2023-06-20 05:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0048_alter_sampleform_requested_export'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sampleform',
            name='requested_export',
            field=models.CharField(choices=[('requested', 'request'), ('export', 'export')], default=None, max_length=155, null=True),
        ),
    ]
