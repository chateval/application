from orm.models import ModelResponse, EvaluationDataset

def get_messages(model_id, evalset_id, get_all=False):
    responses = ModelResponse.objects.filter(model=model_id, evaluationdataset=evalset_id)
    return [{'prompt': response.prompt.prompt_text, 'response': response.response_text} for response in responses]

def get_baselines(evalset_id):
    return EvaluationDataset.objects.get(pk=evalset_id).baselines.filter(is_baseline__gte=1)

def get_latest_baseline(evalset_id):
    return EvaluationDataset.objects.get(pk=evalset_id).baselines.all().latest('model_id')