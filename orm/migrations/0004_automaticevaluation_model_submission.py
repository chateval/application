# Generated by Django 2.0.6 on 2018-07-02 18:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orm', '0003_auto_20180702_1751'),
    ]

    operations = [
        migrations.AddField(
            model_name='automaticevaluation',
            name='model_submission',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.DO_NOTHING, to='orm.ModelSubmission'),
            preserve_default=False,
        ),
    ]
