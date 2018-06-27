from django.shortcuts import render, redirect
from orm.models import Baseline, EvaluationDataset, Model
from orm.scripts import get_messages

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

def models(request):
    models = Model.objects.all()
    datasets = EvaluationDataset.objects.all()
    messages = list()
    evaluations = list()
    if request.method == "POST":
        messages = get_messages(request.POST['model_id'], request.POST['evalset_id'])
        dataset = EvaluationDataset.objects.get(pk=request.POST['evalset_id'])
        for automatic_evaluation in AutomaticEvaluation.objects.filter(model=request.POST['model_id'], 
            evaluationdataset=request.POST['evalset_id']):      
            evaluations.append(dict({'name': automatic_evaluation.metric.name, 'value': automatic_evaluation.value}))
        return render(request, 'models.html', {'POST': True, 'model': Model.objects.get(pk=request.POST['model_id']),
            'messages': messages , 'models': models, 'datasets': datasets, 'dataset': dataset, 'evaluations': evaluations})
    return render(request, 'models.html', {'POST': False, 'models': models, 'datasets': datasets})
