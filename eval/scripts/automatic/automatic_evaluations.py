import requests
import os
from json import dumps as json
from orm.models import AutomaticEvaluation, Metric
from orm.scripts import get_baseline_messages

def run_automatic_evaluation(model, submission, model_responses, evalset):
    model_id = model.model_id
    evalset_id = evalset.pk
    baseline_responses = [message['response'] for message in get_baseline_messages(evalset_id)]
    responses = json({'model_responses': model_responses, 'baseline_responses': baseline_responses})

    r = requests.post('http://' + os.environ['EVAL_LOCATION'] + '/', json=responses).json()

    AutomaticEvaluation.objects.bulk_create([
        AutomaticEvaluation(metric=Metric.objects.get(metric_id=1), model=model, evaluationdataset=evalset, value=r['avg_len'], model_submission=submission),
        AutomaticEvaluation(metric=Metric.objects.get(metric_id=2), model=model, evaluationdataset=evalset, value=r['distinct_1'], model_submission=submission),
        AutomaticEvaluation(metric=Metric.objects.get(metric_id=3), model=model, evaluationdataset=evalset, value=r['distinct_2'], model_submission=submission),
        AutomaticEvaluation(metric=Metric.objects.get(metric_id=4), model=model, evaluationdataset=evalset, value=r['greedy_match'], model_submission=submission),
        AutomaticEvaluation(metric=Metric.objects.get(metric_id=5), model=model, evaluationdataset=evalset, value=r['extrema_score'], model_submission=submission),
        AutomaticEvaluation(metric=Metric.objects.get(metric_id=6), model=model, evaluationdataset=evalset, value=r['average_embedding_score'], model_submission=submission),
    ])