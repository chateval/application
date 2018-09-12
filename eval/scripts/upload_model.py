import os
import datetime
import requests
import boto3
from json import dumps
from boto3 import session
from django.shortcuts import redirect
from orm.models import Model, EvaluationDatasetText, ModelResponse, ModelSubmission, EvaluationDataset, AutomaticEvaluation, Metric
from orm.scripts import get_latest_baseline, get_messages
from chateval.settings import (AWS_ACCESS_KEY, AWS_SECRET_ACCESS_KEY, AWS_STORAGE_BUCKET_NAME, AWS_STORAGE_BUCKET_LOCATION)

def handle_submit(model, dataset, response_file, is_baseline):
    if not is_baseline:
        baseline = get_latest_baseline(dataset.evalset_id)
        baseline_responses = [message['response'] for message in get_messages(baseline, dataset.evalset_id)]
    else:
        baseline_responses = list()
        
    responses = response_file.file.getvalue().decode(encoding='UTF-8').split('\n')
    evaluations = requests.post(os.environ['EVAL_LOCATION'], json=dumps({'model_responses': responses, 'baseline_responses': baseline_responses, 'is_baseline': is_baseline})).json()

    model.save()
    submission = ModelSubmission(model=model, date=datetime.datetime.now().date())
    submission.save()
    submission.evaluationdatasets.add(dataset)
    if is_baseline:
        dataset.baselines.add(model)
        dataset.save()

    save_responses(responses, dataset, model, submission)
    save_evaluations(evaluations, dataset, model, submission, is_baseline)
    upload_file('models/' + str(submission.submission_id) + '-' + response_file.name, response_file)

def upload_file(path, body):
    session = boto3.session.Session(aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
    s3 = session.resource('s3')
    s3.Bucket(AWS_STORAGE_BUCKET_NAME).put_object(Key=path, Body=body)

def save_responses(responses, dataset, model, submission):
    prompts = EvaluationDatasetText.objects.filter(evaluationdataset=dataset)
    model_responses = list()
    for i in range(min(len(responses), len(prompts))):
        model_responses.append(ModelResponse(model_submission=submission, evaluationdataset=dataset, prompt=prompts[i], model=model, response_text=responses[i]))
    ModelResponse.objects.bulk_create(model_responses)

def save_evaluations(evaluations, dataset, model, submission, is_baseline):
    auto_evaluations = [
        AutomaticEvaluation(metric=Metric.objects.get(metric_id=1), model=model, evaluationdataset=dataset, value=evaluations['avg_len'], model_submission=submission),
        AutomaticEvaluation(metric=Metric.objects.get(metric_id=2), model=model, evaluationdataset=dataset, value=evaluations['distinct_1'], model_submission=submission),
        AutomaticEvaluation(metric=Metric.objects.get(metric_id=3), model=model, evaluationdataset=dataset, value=evaluations['distinct_2'], model_submission=submission)
    ]

    if not is_baseline:
        auto_evaluations.append(AutomaticEvaluation(metric=Metric.objects.get(metric_id=7), model=model, evaluationdataset=dataset, value=evaluations['bleu'], model_submission=submission))
        auto_evaluations.append(AutomaticEvaluation(metric=Metric.objects.get(metric_id=6), model=model, evaluationdataset=dataset, value=evaluations['average_embedding_score'], model_submission=submission))
        auto_evaluations.append(AutomaticEvaluation(metric=Metric.objects.get(metric_id=4), model=model, evaluationdataset=dataset, value=evaluations['greedy_match'], model_submission=submission))
        auto_evaluations.append(AutomaticEvaluation(metric=Metric.objects.get(metric_id=5), model=model, evaluationdataset=dataset, value=evaluations['extrema_score'], model_submission=submission))
    
    AutomaticEvaluation.objects.bulk_create(auto_evaluations)