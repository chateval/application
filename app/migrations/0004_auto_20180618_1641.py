# Generated by Django 2.0.6 on 2018-06-18 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_auto_20180618_1636'),
    ]

    operations = [
        migrations.AlterField(
            model_name='evaluationdatasettext',
            name='prompt_id',
            field=models.BigAutoField(primary_key=True, serialize=False),
        ),
    ]