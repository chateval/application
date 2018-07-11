# Generated by Django 2.0.6 on 2018-07-11 20:25

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('orm', '0006_metric_info'),
    ]

    operations = [
        migrations.CreateModel(
            name='HumanEvaluations',
            fields=[
                ('mturk_run_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('submit_datetime', models.DateTimeField()),
                ('results_path', models.TextField()),
                ('evaluationdataset', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='orm.EvaluationDataset')),
                ('model_1', models.ForeignKey(db_column='model_1', on_delete=django.db.models.deletion.DO_NOTHING, related_name='model_1', to='orm.Model')),
                ('model_2', models.ForeignKey(db_column='model_2', on_delete=django.db.models.deletion.DO_NOTHING, related_name='model_2', to='orm.Model')),
            ],
            options={
                'db_table': 'HumanEvaluations',
            },
        ),
        migrations.RenameField(
            model_name='humanevaluationsabcomparison',
            old_name='submit_datetime',
            new_name='accept_datetime',
        ),
        migrations.RenameField(
            model_name='humanevaluationsabcomparison',
            old_name='prompt',
            new_name='prompt_id',
        ),
        migrations.RemoveField(
            model_name='humanevaluationsabcomparison',
            name='evaluationdataset',
        ),
        migrations.RemoveField(
            model_name='humanevaluationsabcomparison',
            name='model_1',
        ),
        migrations.RemoveField(
            model_name='humanevaluationsabcomparison',
            name='model_2',
        ),
        migrations.RemoveField(
            model_name='humanevaluationsabcomparison',
            name='results_path',
        ),
        migrations.AddField(
            model_name='humanevaluationsabcomparison',
            name='mturk_run_id',
            field=models.ForeignKey(default=django.utils.timezone.now, on_delete=django.db.models.deletion.DO_NOTHING, to='orm.HumanEvaluations'),
            preserve_default=False,
        ),
    ]
