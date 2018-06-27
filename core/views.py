from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from .models import Baseline, EvaluationDataset, Model
from .scripts import upload_model, load_responses

def splash(request):
    datasets = EvaluationDataset.objects.all()
    baselines = Baseline.objects.all()
    return render(request, 'splash.html', {'datasets': datasets, 'baselines': baselines})

def conversations(request):
    models = Model.objects.all()
    datasets = EvaluationDataset.objects.all()
    messages = list()
    if request.method == "POST":
        messages = get_messages(request.POST['model_id'], request.POST['evalset_id'])
        return render(request, 'conversations.html', 
            {'POST': True, 'messages': messages, 'models': models, 'datasets': datasets})
    return render(request, 'conversations.html', 
        {'POST': False, 'messages': messages, 'models': models, 'datasets': datasets})

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
                file = dict()
                if request.FILES.get(response_file.name) is not None:
                    file['file'] = request.FILES.get(response_file.name)
                    file['dataset'] = response_file
                    files.append(file)
                    
                    if 'baseline' in form.data.keys():
                        baseline = Baseline(model=model, evaluationdataset=response_file)
                        baseline.save()

            upload_model(model, files, 'baseline' in form.data.keys())
            return HttpResponseRedirect('/evaluation/')
    form = UploadModelForm()
    return render(request, 'submit.html', {'form': form, 'response_files': response_files})   
