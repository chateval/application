# Generated by Django 2.0.7 on 2018-07-30 18:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orm', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='model',
            name='public',
            field=models.BooleanField(default=False),
        ),
    ]
