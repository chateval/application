import datetime
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.utils.encoding import smart_str
from orm.models import Author, Model, EvaluationDataset, Metric, ModelResponse, ModelSubmission
from orm.scripts import get_messages, get_baselines
from eval.scripts.human.launch_hit import launch_hits
from eval.scripts.human.retrieve_responses import retrieve
from eval.scripts.upload_model import handle_submit, send_email, download_file, upload_dbdc5_file
from eval.forms import UploadModelForm, DBDC5Form, SignUpForm, LogInForm

def uploads(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/login')
    current_author = Author.objects.get(author_id=request.user)
    models = Model.objects.filter(author=current_author, archived=False)
    uploads = []
    evalsets = []
    for model in models:
        uploads.append(dict({'model': model, 'evalsets': evalsets}))
    uploads.reverse()
    return render(request, 'uploads.html', {'uploads': uploads})


def human(request):
    model = Model.objects.get(pk=request.GET['id'])
    datasets = EvaluationDataset.objects.all()
    baselines = []
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

def dbdc5download(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/login')
    current_author = Author.objects.get(author_id=request.user)
    send_email("chatevalteam@gmail.com", "Data Request", str(request.user))

    # from https://stackoverflow.com/questions/1156246/having-django-serve-downloadable-files
    return download_file('release-v3-distrib.zip')
    #return redirect("/")

def dbdc5submit(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/login')


    if request.method == "POST":
        name = request.POST['name']
        submission_info = request.POST['submission_info']
        submission_track =  request.POST['submission_track']

        if upload_dbdc5_file('dbdc_submissions/' + str(request.user) + '_' + name + '_' + submission_info + '_' + submission_track, request.FILES['dbdc5file']):
            send_email("chatevalteam@gmail.com", "DBDC5 submission", str(request.user))
            send_email(str(request.user.email), "DBDC5 submission received", "Thank you for your submission")
            return HttpResponseRedirect('https://chateval.org/shared_task')

    form = DBDC5Form()
    error = "error" in request.GET
    return render(request, 'dbdc5submit.html', {'form': form, 'error': error})
    
