from django.http import JsonResponse
from orm.models import Model, ModelResponse, EvaluationDataset, EvaluationDatasetText 

def api(request):
    return JsonResponse({'message': "Welcome to the API!"})

def responses(request):
    responses = ModelResponse.objects.filter(model=request.GET.get('model_id'), evaluationdataset=request.GET.get('evalset')).values()
    return JsonResponse({'responses': list(responses)})

def prompts(request):
    prompts = EvaluationDatasetText.objects.filter(evaluationdataset=request.GET.get('evalset')).values()
    return JsonResponse({'prompts': list(prompts)})

def models(request):
    models = Model.objects.all().values()
    return JsonResponse({'models': list(models)})

def evaluationdatasets(request):
    evaluationdatasets = EvaluationDataset.objects.all().values()
    return JsonResponse({'evaluationdatasets': list(evaluationdatasets)})