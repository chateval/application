import datetime
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from orm.models import Author, Model, EvaluationDataset, Metric, ModelResponse, ModelSubmission
from orm.scripts import get_messages, get_baselines
from eval.scripts.human.launch_hit import launch_hits
from eval.scripts.human.retrieve_responses import retrieve
from eval.scripts.upload_model import handle_submit, send_email
from eval.forms import UploadModelForm, SignUpForm, LogInForm

def uploads(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/login')
    current_author = Author.objects.get(author_id=request.user)
    models = Model.objects.filter(author=current_author, archived=False)
    uploads = list()
    for model in models:
        evalsets = []
        uploads.append(dict({'model': model, 'evalsets': evalsets}))
    uploads.reverse()
    return render(request, 'uploads.html', {'uploads': uploads})


def human(request):
    model = Model.objects.get(pk=request.GET['id'])
    datasets = EvaluationDataset.objects.all()
    baselines = list()
    for dataset in model.evaluationdatasets.all():
        for baseline in dataset.baselines.all():
            baselines.append({"id": baseline.pk, "name": baseline.name, "description": baseline.description, "dataset": dataset})
    return render(request, 'human.html', {'model_id': model.pk, 'baselines': baselines})


def delete(request):
    if request.method == "GET":
        return render(request, 'delete.html', { 'model_id': request.GET['model_id']})
    model = Model.objects.get(pk=request.GET['model_id'])
    model.archived = True
    model.save()
    return redirect('/uploads')


def publish(request):
    if request.method == "GET":
        return render(request, 'publish.html', { 'model_id': request.GET['model_id']})
    model = Model.objects.get(pk=request.GET['model_id'])
    model.public = True
    model.save()
    return redirect('/uploads')


def submit(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/login')

    eval_datasets = EvaluationDataset.objects.all()
    if request.method == "POST":
        model = Model(name=request.POST['name'], author=Author.objects.get(pk=request.user), description=request.POST['description'], repo_location=request.POST['repo_location'], cp_location=request.POST['checkpoint_location'])
        response_files = []
        datasets = []
        for dataset in eval_datasets:
            if dataset.name in request.FILES.keys():
                response_file = request.FILES[dataset.name]
                response_files.append(response_file)
                datasets.append(dataset)
        if handle_submit(model, datasets, response_files, 'baseline' in request.POST):
            return HttpResponseRedirect('/uploads')
        else:
            print(str(request))
            return redirect("/upload?error=input")

    form = UploadModelForm()
    error = "error" in request.GET
    return render(request, 'submit.html', {'form': form, 'response_files': eval_datasets, 'error': error})


def login_view(request):
    if request.method == "POST":
        form = LogInForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                return redirect('/uploads')
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
                            name=form.cleaned_data['first_name'] + " " + form.cleaned_data['last_name'], 
                            institution=form.cleaned_data['institution'],
                            email=form.cleaned_data['email'])
            author.save()
            return redirect('/accounts/login')            
    form = SignUpForm()
    return render(request, 'registration/signup.html', {'form' : form})

def compare(request):
    email_body =  "Model1: " + str(request.GET['model1']) + " | Model2: " + str(request.GET['model2']) + " | Dataset: " + str(request.GET['evalset'])
    send_email("chatevalteam@gmail.com", "System Comparison", email_body)
    return redirect("/")

def dbdc5downlad(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/login')
    current_author = Author.objects.get(author_id=request.user)
    send_email("chatevalteam@gmail.com", "Data Request", str(request.user))
    return redirect("/")
