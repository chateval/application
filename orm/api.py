from django.http import JsonResponse
from django.forms.models import model_to_dict
from orm.models import Model, Metric, ModelResponse, ModelSubmission, AutomaticEvaluation, EvaluationDataset, EvaluationDatasetText, HumanEvaluations, HumanEvaluationsABComparison
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
        "repo_location": model.repo_location, 
        "cp_location": model.cp_location, 
        "evalsets": list(model.evaluationdatasets.all().values())
    }
    return JsonResponse({'model': serialized})

def evaluationdatasets(request):
    evaluationdatasets = EvaluationDataset.objects.all().values()
    return JsonResponse({'evaluationdatasets': list(evaluationdatasets)})

def automatic_evaluations(request):
    eval_metrics = AutomaticEvaluation.objects.filter(
        evaluationdataset=request.GET.get('evaluationdataset_id'), model=request.GET.get('model_id'))

    auto_evals = list()
    for eval in eval_metrics:
        auto_evals.append(dict({'id': eval.metric.metric_id,
                                'name': eval.metric.name,
                                'value': "{0:.3f}".format(eval.value)}))
    return JsonResponse({'evaluations': list(auto_evals)})

def human_evaluations(request):
    target_model_id = request.GET.get('model_id')
    target_model_name = Model.objects.filter(pk=target_model_id).values()[0]['name']
     
    model_comparisons = HumanEvaluations.objects.filter(
        model_1_id=target_model_id,
        evaluationdataset_id=request.GET.get('evaluationdataset_id'))

    # The target model might be stored in the comparison database as model2.
    # Check for this case.
    flipped = False
    if len(model_comparisons) == 0:
        model_comparisons = HumanEvaluations.objects.filter(
            model_2_id=target_model_id,
            evaluationdataset_id=request.GET.get('evaluationdataset_id'))
        flipped = True

    # Return an error if there are no comparisons for this model/eval set combo.
    if len(model_comparisons) == 0:
      return JsonResponse("INVALID_QUERY", safe=False)

    results = []
    for model_comparison in model_comparisons:
        if flipped:
            other_model_id = model_comparison.model_1.model_id
            other_model_name = model_comparison.model_1.name
        else:
            other_model_id = model_comparison.model_2.model_id
            other_model_name = model_comparison.model_2.name

        mturk_run_id = model_comparison.mturk_run_id
        comparisons = HumanEvaluationsABComparison.objects.filter(mturk_run_id=mturk_run_id)
        m1win = 0
        m2win = 0
        tie = 0
        # -1 is a tie, 0 if vote for model 1, 1 is vote for model2
        for comparison in comparisons:
            value = comparison.value
            if value == 0:
                m1win += 1
            elif value == 1:
                m2win += 1
            elif value == -1:
                tie += 1
            else:
                raise ValueError('THIS SHOULD NEVER HAPPEN.')
        if flipped:
            result = {'tie': tie,
                      'm1win': m2win,
                      'm2win': m1win,
                      'model1': target_model_name,
                      'model2': other_model_name
                     }
        else:
            result = {'tie': tie,
                      'm1win': m1win,
                      'm2win': m2win,
                      'model1': target_model_name,
                      'model2': other_model_name
                     }

        results.append(result)

    return JsonResponse({'evaluations': results})
