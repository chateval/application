import datetime
import requests
import boto3
from boto3 import session
from orm.models import EvaluationDatasetText, ModelResponse, ModelSubmission, EvaluationDataset
from orm.scripts import upload_responses
from eval.scripts.automatic_evaluations import run_automatic_evaluation
from chateval.settings import (AWS_ACCESS_KEY, AWS_SECRET_ACCESS_KEY, AWS_STORAGE_BUCKET_NAME, AWS_STORAGE_BUCKET_LOCATION)

def s3_upload_file(path, body):
    session = boto3.session.Session(aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
    s3 = session.resource('s3')
    s3.Bucket(AWS_STORAGE_BUCKET_NAME).put_object(Key=path, Body=body)

def upload_model(model, files, baseline=False):
    model_submission = ModelSubmission(model=model, date=datetime.datetime.now().date())
    model_submission.save()
    
    for file in files:           
        path = 'models/' + str(model_submission.submission_id) + '-' + file['file'].name
        s3_upload_file(path, file['file'])
        upload_responses(AWS_STORAGE_BUCKET_LOCATION + path, file['dataset'], model, model_submission)
        if not baseline:
            run_automatic_evaluation(model, file['dataset'])