from django.http import HttpResponseRedirect
from django.shortcuts import render
from orm.models import Author, Baseline, Model, EvaluationDataset, AutomaticEvaluation, Metric, ModelResponse
from orm.scripts import get_messages
from .scripts.automatic_evaluations import run_automatic_evaluation
from .scripts.upload_model import upload_model
from .forms import UploadModelForm

def my_models(request):
    current_author = Author.objects.get(author_id=request.user)
    models = Model.objects.filter(author=current_author)
    return render(request, 'my_models.html', { 'models': models })

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
            return HttpResponseRedirect('/my_models')
    form = UploadModelForm()
    return render(request, 'submit.html', {'form': form, 'response_files': response_files})   