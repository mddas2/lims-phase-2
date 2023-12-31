# Generated by Django 4.1 on 2023-07-31 08:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0136_mandatorystandard_testmethod_units_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='rawdatasheetdetail',
            name='mandatory_standard',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='rawdatasheetdetail',
            name='test_method',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='rawdatasheetdetail',
            name='units',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='sampleformparameterformulacalculate',
            name='mandatory_standard',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='sampleformparameterformulacalculate',
            name='test_method',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='sampleformparameterformulacalculate',
            name='units',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
