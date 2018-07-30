from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from orm.models import Author, Baseline, Model, EvaluationDataset, Metric, ModelResponse, ModelSubmission
from orm.scripts import get_messages
from eval.scripts.human.launch_hit import launch_hits
from eval.scripts.human.retrieve_responses import retrieve
from eval.scripts.upload_model import upload_model
from eval.forms import UploadModelForm

def uploads(request):
    current_author = Author.objects.get(author_id=request.user)
    models = Model.objects.filter(author=current_author, archived=False)
    uploads = list()
    for model in models:
        submission = ModelSubmission.objects.filter(model=model)[0]
        evalsets = [evalset.name for evalset in submission.evaluationdatasets.all()]
        uploads.append(dict({'model': model, 'evalsets': evalsets}))
    uploads.reverse()
    return render(request, 'uploads.html', { 'uploads': uploads })

def delete(request):
    return render(request, 'delete.html', { 'model_id': request.GET['model_id']})

def publish(request):
    if request.method == "GET":
        return render(request, 'publish.html', { 'model_id': request.GET['model_id']})

def submit(request):
    response_files = EvaluationDataset.objects.all()
    if request.method == "POST":
        form = UploadModelForm(request.POST, request.FILES)
        if form.is_valid():
            model = Model(author=Author.objects.get(pk=request.user),
                name=form.cleaned_data['name'],
                description=form.cleaned_data['description'],
                repo_location = form.cleaned_data['repo_location'],
                cp_location=form.cleaned_data['checkpoint_location'])
            model.save()

            files = list()
            for response_file in response_files:
                if response_file.name in request.FILES.keys():
                    files.append({'file': request.FILES[response_file.name], 'dataset': response_file})               
                    if 'baseline' in form.data.keys():
                        baseline = Baseline(model=model, evaluationdataset=response_file)
                        baseline.save()
            upload_model(model, files, 'baseline' in form.data.keys())
            return HttpResponseRedirect('/uploads')
    form = UploadModelForm()
    return render(request, 'submit.html', {'form': form, 'response_files': response_files})   

def human(request):
    print("\n\n")
    print(request.POST['model_id'])
    model = Model.objects.get(model_id=request.POST['model_id'])
    baseline_model = Model.objects.filter(name="Human Baseline")[0]
    evalset = EvaluationDataset.objects.filter(name="NCM")[0]
    launch_hits(evalset, baseline_model, model)
    #retrieve() 
    return redirect('/model')