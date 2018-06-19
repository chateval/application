import boto3
from boto3 import session
from django.shortcuts import render, redirect
from .models import Dataset, Baseline
from .generate_prompts import load_dataset
from .link_responses import load_responses
from .forms import UploadModelForm
from chateval.settings import AWS_ACCESS_KEY, AWS_SECRET_ACCESS_KEY, AWS_STORAGE_BUCKET_NAME

def splash(request):
    datasets = Dataset.objects.all()
    baselines = Baseline.objects.all()
    return render(request, 'splash.html', {'datasets': datasets, 'baselines': baselines})

def models(request):
    return render(request, 'models.html', {})

def conversations(request):
    return render(request, 'conversations.html', {})

def submit(request):
    if request.method == "POST":
        response_dataset = request.FILES.get('response_dataset')
        file_path = 'models/' + response_dataset.name
        session = boto3.session.Session(aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
        s3 = session.resource('s3')
        s3.Bucket(AWS_STORAGE_BUCKET_NAME).put_object(Key=file_path, Body=response_dataset)
        redirect('/')
    form = UploadModelForm()
    return render(request, 'submit.html', {'form': form})
    
