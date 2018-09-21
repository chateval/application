import datetime
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from orm.models import Author, Model, EvaluationDataset, Metric, ModelResponse, ModelSubmission
from eval.scripts.human.launch_hit import launch_hits
from eval.scripts.human.retrieve_responses import retrieve
from eval.scripts.upload_model import handle_submit
from eval.forms import UploadModelForm

def uploads(request):
    current_author = Author.objects.get(author_id=request.user)
    models = Model.objects.filter(author=current_author, archived=False)
    uploads = list()
    for model in models:
        evalsets = []
        uploads.append(dict({'model': model, 'evalsets': evalsets}))
    uploads.reverse()
    return render(request, 'uploads.html', {'uploads': uploads})

def human(request):
    return render(request, 'human_demo.html', {})

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

    datasets = EvaluationDataset.objects.all()
    if request.method == "POST":
        model = Model(name=request.POST['name'], author=Author.objects.get(pk=request.user), description=request.POST['description'], repo_location=request.POST['repo_location'], cp_location=request.POST['checkpoint_location'])
        for dataset in datasets:
            if dataset.name in request.FILES.keys():
                response_file = request.FILES[dataset.name]
                handle_submit(model, dataset, response_file, 'baseline' in request.POST)
        return HttpResponseRedirect('/uploads')

    form = UploadModelForm()
    return render(request, 'submit.html', {'form': form, 'response_files': datasets})

'''def human(request):
    print("\n\n")
    print(request.POST['model_id'])
    model = Model.objects.get(model_id=request.POST['model_id'])
    baseline_model = Model.objects.filter(name="Human Baseline")[0]
    evalset = EvaluationDataset.objects.filter(name="NCM")[0]
    launch_hits(evalset, baseline_model, model)
    #retrieve() 
    return redirect('/uploads')'''