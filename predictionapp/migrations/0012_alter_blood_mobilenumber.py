# Generated by Django 4.1.5 on 2023-02-15 05:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('predictionapp', '0011_rename_mobile_blood_mobilenumber'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blood',
            name='mobilenumber',
            field=models.IntegerField(blank=True, max_length=100, null=True),
        ),
    ]