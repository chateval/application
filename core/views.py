from django.shortcuts import render, redirect
from orm.models import Baseline, EvaluationDataset, Model, AutomaticEvaluation, ModelSubmission, Metric
from orm.scripts import get_messages

def splash(request):
    datasets = EvaluationDataset.objects.all()
    baselines = Baseline.objects.all()
    metrics = Metric.objects.all()
    return render(request, 'splash.html', {'datasets': datasets, 'baselines': baselines, 'metrics': metrics})

def conversations(request):
    models = Model.objects.filter(archived=False)
    datasets = EvaluationDataset.objects.all()
    if request.GET.get('model_id') is not None and request.GET.get('evalset_id') is not None:
        messages = get_messages(request.GET.get('model_id'), request.GET.get('evalset_id'))
        return render(request, 'conversations.html', {'GET': True, 'messages': messages, 
                                            'models': models, 'datasets': datasets})
    return render(request, 'conversations.html', {'GET': False, 'messages': list(), 
                                            'models': models, 'datasets': datasets})

def model(request):
    models = Model.objects.filter(archived=False)
    if request.GET.get('model_id') is not None and request.GET.get('model_id') is not None:
        messages = get_messages(request.GET.get('model_id'), request.GET.get('evalset_id'), get_all=False)
        submission = ModelSubmission.objects.filter(model=request.GET.get('model_id'))[0]
        evaluations = list()
        for evalset in submission.evaluationdatasets.all():
            auto_evals = list()
            for eval in AutomaticEvaluation.objects.filter(model_submission=submission, evaluationdataset=evalset):
                auto_evals.append(dict({'id': eval.metric.metric_id, 'name': eval.metric.name, 'value': "{0:.3f}".format(eval.value)}))
            evaluations.append(dict({'evalset': evalset, 'auto_evals': auto_evals}))
        return render(request, 'model.html', {'GET': True, 'model': Model.objects.get(pk=request.GET.get('model_id')),
                                                'messages': messages , 'models': models, 'evaluations': evaluations})
    return render(request, 'model.html', {'GET': False, 'models': models})
