from django.http import JsonResponse
from orm.models import Model, ModelResponse, ModelSubmission, AutomaticEvaluation, EvaluationDataset, EvaluationDatasetText 

def api(request):
    return JsonResponse({'message': "Welcome to the API!"})

def responses(request):
    if Model.objects.get(pk=request.GET['model_id']).public == True and Model.objects.get(pk=request.GET['model_id']).archived == False:
        responses = ModelResponse.objects.filter(model=request.GET['model_id'], evaluationdataset=request.GET['evalset']).values()
        return JsonResponse({'responses': list(responses)})
    return JsonResponse({'message': "Model is not public."})

def prompts(request):
    prompts = EvaluationDatasetText.objects.filter(evaluationdataset=request.GET.get('evalset')).values()
    return JsonResponse({'prompts': list(prompts)})

def models(request):
    models = Model.objects.filter(public=True, archived=False).values()
    return JsonResponse({'models': list(models)})

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