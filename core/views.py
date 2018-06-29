from django.shortcuts import render, redirect
from orm.models import Baseline, EvaluationDataset, Model, AutomaticEvaluation
from orm.scripts import get_messages

def splash(request):
    datasets = EvaluationDataset.objects.all()
    baselines = Baseline.objects.all()
    return render(request, 'splash.html', {'datasets': datasets, 'baselines': baselines})

def conversations(request):
    models = Model.objects.all()
    datasets = EvaluationDataset.objects.all()
    messages = list()
    if request.GET.get('model_id') is not None and request.GET.get('evalset_id') is not None:
        messages = get_messages(request.GET.get('model_id'), request.GET.get('evalset_id'))
        return render(request, 'conversations.html', 
            {'GET': True, 'messages': messages, 'models': models, 'datasets': datasets})
    return render(request, 'conversations.html', 
        {'GET': False, 'messages': messages, 'models': models, 'datasets': datasets})

def models(request):
    models = Model.objects.all()
    datasets = EvaluationDataset.objects.all()
    messages = list()
    evaluations = list()
    if request.GET.get('model_id') is not None and request.GET.get('model_id') is not None:
        messages = get_messages(request.GET.get('model_id'), request.GET.get('evalset_id'), get_all=False)
        dataset = EvaluationDataset.objects.get(pk=request.GET.get('evalset_id'))
        for auto in AutomaticEvaluation.objects.filter(model=request.GET.get('model_id'), 
            evaluationdataset=request.GET.get('evalset_id')):
            evaluations.append(dict({'name': auto.metric.name, 'value': "{0:.3f}".format(auto.value), 'info': auto.metric.info}))
        return render(request, 'models.html', {'GET': True, 'model': Model.objects.get(pk=request.GET.get('model_id')),
            'messages': messages , 'models': models, 'datasets': datasets, 'dataset': dataset, 'evaluations': evaluations})
    return render(request, 'models.html', {'GET': False, 'models': models, 'datasets': datasets})
