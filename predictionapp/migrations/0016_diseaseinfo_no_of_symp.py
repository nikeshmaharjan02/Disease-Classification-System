# Generated by Django 4.1.5 on 2023-04-10 12:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('predictionapp', '0015_alter_blood_mobilenumber'),
    ]

    operations = [
        migrations.AddField(
            model_name='diseaseinfo',
            name='no_of_symp',
            field=models.IntegerField(default=0),
        ),
    ]
