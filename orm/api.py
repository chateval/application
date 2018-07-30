from django.http import JsonResponse
from orm.models import Model, ModelResponse, EvaluationDataset, EvaluationDatasetText 

def api(request):
    return JsonResponse({'message': "Welcome to the API!"})

def responses(request):
    responses = ModelResponse.objects.filter(model=request.GET.get('model_id'), evaluationdataset=request.GET.get('evalset')).values()
    return JsonResponse({'responses': list(responses)})