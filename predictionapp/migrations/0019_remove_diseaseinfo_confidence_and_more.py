# Generated by Django 4.1.5 on 2023-04-11 02:32

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('predictionapp', '0018_diseaseinfo_confidence'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='diseaseinfo',
            name='confidence',
        ),
        migrations.AddField(
            model_name='diseaseinfo',
            name='symptomsname',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=200), default=list, size=None),
        ),
    ]