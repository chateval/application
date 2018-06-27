import datetime
import requests
import boto3
from boto3 import session
from .models import EvaluationDatasetText, ModelResponse, ModelSubmission, EvaluationDataset
from eval.views import run_automatic_evaluation
from chateval.settings import (AWS_ACCESS_KEY, AWS_SECRET_ACCESS_KEY, 
    AWS_STORAGE_BUCKET_NAME, AWS_STORAGE_BUCKET_LOCATION)

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
        print("saved to s3 and loading responses")
        load_responses(AWS_STORAGE_BUCKET_LOCATION + path, file['dataset'], model, model_submission)
        print("running automatic eval")
        run_automatic_evaluation(model, dataset)

def load_responses(response_file, dataset, model, submission):
    response = requests.get(response_file)
    data = response.text
    responses = data.split('\n')
    prompts = EvaluationDatasetText.objects.all().filter(evaluationdataset=dataset)
    
    model_responses = list()
    for i in range(len(responses)):
        model_response = ModelResponse(model_submission=submission, evaluationdataset=dataset, 
            prompt=prompts[i], model=model, response_text=responses[i])
        model_responses.append(model_response)
    ModelResponse.objects.bulk_create(model_responses)