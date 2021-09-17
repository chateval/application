"""Functions for submitting models,  launching evaluation, and saving results to the database."""

import os
import datetime
import requests
import gzip
import boto3
import smtplib
from email.message import EmailMessage
from json import dumps
from boto3 import session
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from orm.models import Model, EvaluationDatasetText, ModelResponse, ModelSubmission, EvaluationDataset, AutomaticEvaluation, Metric
from orm.scripts import get_latest_baseline, get_messages
from chateval.settings import (AWS_ACCESS_KEY, AWS_SECRET_ACCESS_KEY, AWS_STORAGE_BUCKET_NAME, AWS_STORAGE_BUCKET_LOCATION)

def handle_submit(model, datasets, response_files, is_baseline):
    responses, evaluations = [], []
    for i in range(len(datasets)):
        if not is_baseline:
            baseline = get_latest_baseline(datasets[i].evalset_id)
            baseline_responses = [message['response'] for message in get_messages(baseline, datasets[i].evalset_id)]
        else:
            baseline_responses = list()
        
        response = response_files[i].file.getvalue().decode(encoding='UTF-8').split('\n')[0:len(baseline_responses)]
        responses.append(response)
        try:
            evaluations.append(requests.post(os.environ['EVAL_LOCATION'], json=dumps({'model_responses': response, 'baseline_responses': baseline_responses, 'is_baseline': is_baseline})).json())
        except:
            return False
    
    model.save()
            
    for dataset in datasets:
        model.evaluationdatasets.add(dataset)
    
    submission = ModelSubmission(model=model, date=datetime.datetime.now().date())
    submission.save()

    for dataset in datasets:
        submission.evaluationdatasets.add(dataset)

    if is_baseline:
        for dataset in datasets:
            dataset.baselines.add(model)
            dataset.save()

    for i in range(len(datasets)):
        save_responses(responses[i], datasets[i], model, submission)
        save_evaluations(evaluations[i], datasets[i], model, submission, is_baseline)

    for response_file in response_files:
        upload_file('models/' + str(submission.submission_id) + '-' + response_file.name, response_file)
    
    return True

def upload_file(path, body):
    session = boto3.session.Session(aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
    s3 = session.resource('s3')
    s3.Bucket(AWS_STORAGE_BUCKET_NAME).put_object(Key=path, Body=body)

def upload_dbdc5_file(path, body):
    session = boto3.session.Session(aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
    s3 = session.resource('s3')
    if s3.Bucket(AWS_STORAGE_BUCKET_NAME).put_object(Key=path, Body=body):
        return True
    else:
        return False

def upload_dstc10_file(path, body):
    session = boto3.session.Session(aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
    s3 = session.resource('s3')
    # NOTE: this doesn't work :(
    #fileobj = gzip.GzipFile(fileobj=body, mode='rb')
    #path = path + ".gz"
    if s3.Bucket(AWS_STORAGE_BUCKET_NAME).upload_fileobj(Fileobj=fileobj, Key=path):
        return True
    else:
        return False

    
def download_file(filename):
    session = boto3.session.Session(aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
    s3 = session.client('s3')
    url = s3.generate_presigned_url(ClientMethod='get_object', Params={'Bucket': AWS_STORAGE_BUCKET_NAME, 'Key': filename}, ExpiresIn=600)

    return HttpResponseRedirect(url)


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

def send_email(to, subject, content):
    # Construct email.
    message = EmailMessage()
    message['From'] = "chatevalteam@gmail.com"
    message['To'] = to
    message['Subject'] = subject
    message.set_content(content)

    # Open up SMPTP server and send email notification.
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    print(os.environ['EMAIL_PASSWORD'])
    server.login("chatevalteam", str(os.environ['EMAIL_PASSWORD']))
    server.send_message(message)
    server.quit()
