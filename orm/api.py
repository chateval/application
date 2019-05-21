from django.http import JsonResponse
from django.forms.models import model_to_dict
from orm.models import Model, Metric, ModelResponse, ModelSubmission, AutomaticEvaluation, EvaluationDataset, EvaluationDatasetText 
from orm.scripts import get_baselines

def metrics(request):
    return JsonResponse({'metrics': list(Metric.objects.all().values())})

def api(request):
    return JsonResponse({'message': "Welcome to the API!"})

def baselines(request):
    datasets = EvaluationDataset.objects.all()
    baselines = list()
    for dataset in datasets:
        baselines += get_baselines(dataset.pk).values()
    return JsonResponse({'baselines': list(baselines)})

def responses(request):
    responses = ModelResponse.objects.filter(model=request.GET['model_id'], evaluationdataset=request.GET['evalset']).values()
    return JsonResponse({'responses': list(responses)})

def prompts(request):
    prompts = EvaluationDatasetText.objects.filter(evaluationdataset=request.GET.get('evalset')).values()
    return JsonResponse({'prompts': list(prompts)})

def models(request):
    models = Model.objects.all()
    serialized = []
    for i, model in enumerate(models):
        serialized.append({"id": model.pk, "name": model.name, "description": model.description, "evalsets": list(model.evaluationdatasets.all().values())})
    return JsonResponse({'models': list(serialized)})

def model(request):
    model = Model.objects.get(pk=request.GET['id'])
    serialized = { 
        "id": model.pk, 
        "name": model.name, 
        "description": model.description, 
        "evalsets": list(model.evaluationdatasets.all().values())
    }
    return JsonResponse({'model': serialized})

def evaluationdatasets(request):
    evaluationdatasets = EvaluationDataset.objects.all().values()
    return JsonResponse({'evaluationdatasets': list(evaluationdatasets)})

def automatic_evaluations(request):
    submission = ModelSubmission.objects.filter(model=request.GET.get('model_id'))[0]
    evaluations = list()
    for evalset in submission.evaluationdatasets.all().values():
        auto_evals = list()
        for eval in AutomaticEvaluation.objects.filter(model_submission=submission, evaluationdataset=evalset['evalset_id']):
            auto_evals.append(dict({'id': eval.metric.metric_id, 'name': eval.metric.name, 'value': "{0:.3f}".format(eval.value)}))
        evaluations.append(dict({'evalset': evalset, 'auto_evals': auto_evals}))
    return JsonResponse({'evaluations': list(evaluations)})