# Generated by Django 2.0.6 on 2018-06-21 19:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_remove_modelresponse_model_submission'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='metric',
            table='Metrics',
        ),
    ]