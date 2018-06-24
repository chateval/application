from django.shortcuts import render
from core.models import Author, Model, EvaluationDataset
from core.views import get_messages
import eval.auto_eval_utils as aeu

def my_models(request):
    current_author = Author.objects.get(author_id=request.user)
    models = Model.objects.filter(author=current_author)
    return render(request, 'my_models.html', {'models': models})

def models(request):
    models = Model.objects.all()
    datasets = EvaluationDataset.objects.all()
    messages = list()
    if request.method == "POST":
        messages = get_messages(request.POST['model_id'], request.POST['evalset_id'])
        dataset = EvaluationDataset.objects.get(pk=request.POST['evalset_id'])
        eval_messages = [message['response'] for message in messages]
        eval = dict()
        eval['avg_len'] = aeu.avg_len(eval_messages)
        return render(request, 'models.html', {'POST': True, 'model': Model.objects.get(pk=request.POST['model_id']), 'messages': messages , 'models': models, 'datasets': datasets, 'dataset': dataset, 'eval': eval})
    return render(request, 'models.html', {'POST': False, 'models': models, 'datasets': datasets})