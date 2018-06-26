from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
import requests

class Baseline(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()

    class Meta:
        db_table = 'Baseline'

class Author(models.Model):
    author_id = models.ForeignKey(settings.AUTH_USER_MODEL, primary_key=True, on_delete=models.CASCADE,)
    name = models.CharField(unique=True, max_length=100)
    email = models.CharField(unique=True, max_length=200)
    institution = models.TextField()

    class Meta:
        db_table = 'Author'

class Model(models.Model):
    model_id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    author = models.ForeignKey(Author, models.DO_NOTHING)
    cp_location = models.TextField()
    repo_location = models.TextField()
    comments = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'Model'
    
class ModelSubmission(models.Model):
    submission_id = models.BigAutoField(primary_key=True)
    date = models.DateTimeField()
    model = models.ForeignKey('Model', models.DO_NOTHING)
    
    class Meta:
        db_table = 'ModelSubmission'

class Metric(models.Model):
    metric_id = models.BigAutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=100)

    class Meta:
        db_table = 'Metrics'


class EvaluationDataset(models.Model):
    evalset_id = models.BigAutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=100)
    long_name = models.CharField(unique=True, max_length=255)
    source = models.TextField()
    description = models.TextField()

    class Meta:
        db_table = 'EvaluationDataset'

def save_evaluation_dataset(sender, instance, **kwargs):
    response = requests.get(instance.source)
    data = response.text
    prompts = data.split('\n')

    for prompt in prompts:
        evaluation_dataset_text = EvaluationDatasetText(evaluationdataset=instance, prompt_text=prompt, num_turns=1)
        evaluation_dataset_text.save()

post_save.connect(save_evaluation_dataset, sender=EvaluationDataset)
        
class EvaluationDatasetText(models.Model):
    evaluationdataset = models.ForeignKey(EvaluationDataset, models.DO_NOTHING)
    prompt_id = models.BigAutoField(primary_key=True)
    prompt_text = models.TextField()
    num_turns = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'EvaluationDatasetText'
        unique_together = (('evaluationdataset', 'prompt_id'),)

class ModelResponse(models.Model):
    model = models.ForeignKey('Model', models.DO_NOTHING)
    evaluationdataset = models.ForeignKey(EvaluationDataset, models.DO_NOTHING, related_name='evaluationdatasets')
    prompt = models.ForeignKey(EvaluationDatasetText, models.DO_NOTHING)
    response_text = models.TextField()
    model_submission = models.ForeignKey(ModelSubmission, models.DO_NOTHING)
    is_baseline = models.NullBooleanField()

    class Meta:
        db_table = 'ModelResponse'
        unique_together = (('evaluationdataset', 'model', 'prompt'),)

class AutomaticEvaluation(models.Model):
    id = models.BigAutoField(primary_key=True)
    model = models.ForeignKey('Model', models.DO_NOTHING)
    metric = models.ForeignKey('Metric', models.DO_NOTHING)
    evaluationdataset = models.ForeignKey('EvaluationDataset', models.DO_NOTHING)
    value = models.FloatField()

    class Meta:
        db_table = 'AutomaticEvaluations'
        unique_together = (('model', 'metric', 'evaluationdataset'),)

class HumanEvaluationsABComparison(models.Model):
    model_1 = models.ForeignKey('Model', models.DO_NOTHING, db_column='model_1', related_name='model_1')
    model_2 = models.ForeignKey('Model', models.DO_NOTHING, db_column='model_2', related_name='model_2')
    evaluationdataset = models.ForeignKey(EvaluationDataset, models.DO_NOTHING)
    prompt = models.ForeignKey(EvaluationDatasetText, models.DO_NOTHING, related_name='prompts')
    worker_id = models.CharField(max_length=100)
    hit = models.CharField(db_column='HIT', max_length=100)
    submit_datetime = models.DateTimeField()
    results_path = models.TextField()
    value = models.IntegerField()

    class Meta:
        db_table = 'HumanEvaluationsABComparison'