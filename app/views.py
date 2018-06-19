import boto3
from boto3 import session
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .models import Dataset, Baseline
from .auto_models import Author
from .generate_prompts import load_dataset
from .link_responses import load_responses
from .forms import UploadModelForm, LogInForm, SignUpForm
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

def login_view(request):
    if request.method == "POST":
        form = LogInForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            print(user)
            print(user is not None)
            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                return redirect('/accounts/login')
    form = LogInForm()
    return render(request, 'registration/login.html', {'form' : form})

def signup_view(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(username=form.cleaned_data['username'],
                                 email=form.cleaned_data['email'],
                                 password=form.cleaned_data['password'],
                                 first_name=form.cleaned_data['first_name'],
                                 last_name=form.cleaned_data['last_name'])
            author = Author(author_id=user,
                            name=form.cleaned_data['first_name'] + form.cleaned_data['last_name'], 
                            institution=form.cleaned_data['institution'],
                            email=form.cleaned_data['email'])
            author.save()
            return redirect('/accounts/login')            
    form = SignUpForm()
    return render(request, 'registration/signup.html', {'form' : form})
