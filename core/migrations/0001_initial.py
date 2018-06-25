# Generated by Django 2.0.6 on 2018-06-25 06:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('author_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('name', models.CharField(max_length=100, unique=True)),
                ('email', models.CharField(max_length=200, unique=True)),
                ('institution', models.TextField()),
            ],
            options={
                'db_table': 'Author',
            },
        ),
        migrations.CreateModel(
            name='Baseline',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField()),
            ],
            options={
                'db_table': 'Baseline',
            },
        ),
        migrations.CreateModel(
            name='EvaluationDataset',
            fields=[
                ('evalset_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100, unique=True)),
                ('long_name', models.CharField(max_length=255, unique=True)),
                ('source', models.TextField()),
                ('description', models.TextField()),
            ],
            options={
                'db_table': 'EvaluationDataset',
            },
        ),
        migrations.CreateModel(
            name='EvaluationDatasetText',
            fields=[
                ('prompt_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('prompt_text', models.TextField()),
                ('num_turns', models.IntegerField(blank=True, null=True)),
                ('evaluationdataset', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='core.EvaluationDataset')),
            ],
            options={
                'db_table': 'EvaluationDatasetText',
            },
        ),
        migrations.CreateModel(
            name='HumanEvaluationsABComparison',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('worker_id', models.CharField(max_length=100)),
                ('hit', models.CharField(db_column='HIT', max_length=100)),
                ('submit_datetime', models.DateTimeField()),
                ('results_path', models.TextField()),
                ('value', models.IntegerField()),
                ('evaluationdataset', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='core.EvaluationDatasetText')),
            ],
            options={
                'db_table': 'HumanEvaluationsABComparison',
            },
        ),
        migrations.CreateModel(
            name='Metric',
            fields=[
                ('metric_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
            options={
                'db_table': 'Metrics',
            },
        ),
        migrations.CreateModel(
            name='Model',
            fields=[
                ('model_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255, unique=True)),
                ('description', models.TextField()),
                ('cp_location', models.TextField()),
                ('repo_location', models.TextField()),
                ('comments', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'Model',
            },
        ),
        migrations.CreateModel(
            name='ModelResponse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('response_text', models.TextField()),
                ('evaluationdataset', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='evaluationdatasets', to='core.EvaluationDataset')),
            ],
            options={
                'db_table': 'ModelResponse',
            },
        ),
        migrations.CreateModel(
            name='ModelSubmission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField()),
            ],
            options={
                'db_table': 'ModelSubmission',
            },
        ),
        migrations.CreateModel(
            name='AutomaticEvaluation',
            fields=[
                ('model', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='core.Model')),
                ('value', models.FloatField()),
                ('evaluationdataset', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='core.EvaluationDataset')),
                ('metric', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='core.Metric')),
            ],
            options={
                'db_table': 'AutomaticEvaluations',
            },
        ),
        migrations.AddField(
            model_name='modelsubmission',
            name='model',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='core.Model'),
        ),
        migrations.AddField(
            model_name='modelresponse',
            name='model',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='core.Model'),
        ),
        migrations.AddField(
            model_name='modelresponse',
            name='prompt',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='core.EvaluationDatasetText'),
        ),
        migrations.AddField(
            model_name='model',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='core.Author'),
        ),
        migrations.AddField(
            model_name='humanevaluationsabcomparison',
            name='model_1',
            field=models.ForeignKey(db_column='model_1', on_delete=django.db.models.deletion.DO_NOTHING, related_name='model_1', to='core.Model'),
        ),
        migrations.AddField(
            model_name='humanevaluationsabcomparison',
            name='model_2',
            field=models.ForeignKey(db_column='model_2', on_delete=django.db.models.deletion.DO_NOTHING, related_name='model_2', to='core.Model'),
        ),
        migrations.AddField(
            model_name='humanevaluationsabcomparison',
            name='prompt',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='prompts', to='core.EvaluationDatasetText'),
        ),
        migrations.AlterUniqueTogether(
            name='modelresponse',
            unique_together={('evaluationdataset', 'model', 'prompt')},
        ),
        migrations.AlterUniqueTogether(
            name='evaluationdatasettext',
            unique_together={('evaluationdataset', 'prompt_id')},
        ),
        migrations.AlterUniqueTogether(
            name='automaticevaluation',
            unique_together={('model', 'metric', 'evaluationdataset')},
        ),
    ]
