# Generated by Django 4.1 on 2023-07-01 12:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0080_sampleformhasparameter_super_visor_sample_form_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='supervisorsampleform',
            name='is_analyst_test',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='supervisorsampleform',
            name='status',
            field=models.CharField(blank=True, choices=[('pending', 'pending'), ('not_assigned', 'not_assigned'), ('processing', 'processing'), ('completed', 'completed'), ('recheck', 'recheck'), ('rejected', 'rejected'), ('not_verified', 'not_verified'), ('verified', 'verified')], default='not_assigned', max_length=155, null=True),
        ),
    ]
