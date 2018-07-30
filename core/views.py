from django.shortcuts import render, redirect
from orm.models import Baseline, EvaluationDataset, Model, AutomaticEvaluation, ModelSubmission, Metric, HumanEvaluations, HumanEvaluationsABComparison
from orm.scripts import get_messages

def splash(request):
    datasets = EvaluationDataset.objects.all()
    baselines = Baseline.objects.all()
    metrics = Metric.objects.all()
    return render(request, 'splash.html', {'datasets': datasets, 'baselines': baselines, 'metrics': metrics})

def conversations(request):
    models = Model.objects.all()
    datasets = EvaluationDataset.objects.all()
    if request.GET.get('model_id') is not None and request.GET.get('evalset_id') is not None:
        messages = get_messages(request.GET.get('model_id'), request.GET.get('evalset_id'))
        return render(request, 'conversations.html', {'GET': True, 'messages': messages, 
                                            'models': models, 'datasets': datasets})
    return render(request, 'conversations.html', {'GET': False, 'messages': list(), 
                                            'models': models, 'datasets': datasets})

def model(request):
    models = Model.objects.all()
    if request.GET.get('model_id') is not None and request.GET.get('model_id') is not None:
        # Queries to get the vote results for all the comparisons 
        humanevaluations_1 = HumanEvaluations.objects.filter(model_1=Model.objects.get(pk=request.GET.get('model_id')))
        humanevaluations_2 = HumanEvaluations.objects.filter(model_2=Model.objects.get(pk=request.GET.get('model_id')))
        results = dict()
        for humaneval in humanevaluations_1:
            votes = HumanEvaluationsABComparison.objects.filter(mturk_run_id=humaneval.mturk_run_id)
            wins = 0
            losses = 0
            ties = 0
            for vote in votes:
                if vote.value == 1:
                    wins += 1
                elif vote.value == -1:
                    losses += 1
                else:
                    ties += 1
            results[humaneval.model_2.name] = [wins, losses, ties]

        for humaneval in humanevaluations_2:
            votes = HumanEvaluationsABComparison.objects.filter(mturk_run_id=humaneval.mturk_run_id)
            wins = 0
            losses = 0
            ties = 0
            for vote in votes:
                if vote.value == 1:
                    losses += 1
                elif vote.value == -1:
                    wins += 1
                else:
                    ties += 1
            results[humaneval.model_1.name] = [wins, losses, ties]
                
        print("Results:")
        print(results)
        messages = get_messages(request.GET.get('model_id'), request.GET.get('evalset_id'), get_all=False)
        submission = ModelSubmission.objects.filter(model=request.GET.get('model_id'))[0]
        evaluations = list()
        for evalset in submission.evaluationdatasets.all():
            auto_evals = list()
            for eval in AutomaticEvaluation.objects.filter(model_submission=submission, evaluationdataset=evalset):
                auto_evals.append(dict({'id': eval.metric.metric_id, 'name': eval.metric.name, 'value': "{0:.3f}".format(eval.value)}))
            evaluations.append(dict({'evalset': evalset, 'auto_evals': auto_evals}))
        return render(request, 'model.html', {'GET': True, 'model': Model.objects.get(pk=request.GET.get('model_id')),
                                                'messages': messages , 'models': models, 'evaluations': evaluations, 'results':results})
    return render(request, 'model.html', {'GET': False, 'models': models})
