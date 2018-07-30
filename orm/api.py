from django.http import JsonResponse
from orm.models import Model, ModelResponse, EvaluationDataset, EvaluationDatasetText 

def api(request):
    return JsonResponse({'message': "Welcome to the API!"})

def responses(request):
    if Model.get(pk=request.GET['model_id']).public == True:
        responses = ModelResponse.objects.filter(model=request.GET['model_id'], evaluationdataset=request.GET['evalset']).values()
        return JsonResponse({'responses': list(responses)})
    return return JsonResponse({'message': "Model is not public."})

def prompts(request):
    prompts = EvaluationDatasetText.objects.filter(evaluationdataset=request.GET.get('evalset')).values()
    return JsonResponse({'prompts': list(prompts)})

def models(request):
    models = Model.objects.filter(public=True).values()
    return JsonResponse({'models': list(models)})

def evaluationdatasets(request):
    evaluationdatasets = EvaluationDataset.objects.all().values()
    return JsonResponse({'evaluationdatasets': list(evaluationdatasets)})