# Generated by Django 4.1.5 on 2023-02-15 05:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('predictionapp', '0009_rename_bloodgroup_blood_blood_group'),
    ]

    operations = [
        migrations.RenameField(
            model_name='blood',
            old_name='blood_group',
            new_name='bloodgroup',
        ),
    ]
