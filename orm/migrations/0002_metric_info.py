# Generated by Django 2.0.6 on 2018-06-29 16:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orm', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='metric',
            name='info',
            field=models.CharField(default='github.com', max_length=200),
            preserve_default=False,
        ),
    ]
