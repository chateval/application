from gensim.models import KeyedVectors
from orm.models import AutomaticEvaluation, Metric
from orm.scripts import get_messages, get_baseline_messages
from .auto_eval_utils import avg_len, distinct_1, distinct_2

def run_automatic_evaluation(model, evalset):
    model_id = model.model_id
    evalset_id = evalset.pk
    model_responses = [message['response'] for message in get_messages(model_id, evalset_id)]
    baseline_responses = [message['response'] for message in get_baseline_messages(evalset_id)]

    w2v = KeyedVectors.load_word2vec_format("./files/google_news_vectors.gz", binary=True)

    AutomaticEvaluation.objects.bulk_create([
        AutomaticEvaluation(metric=Metric.objects.get(metric_id=1), model=model, evaluationdataset=evalset, value=avg_len(model_responses)),
        AutomaticEvaluation(metric=Metric.objects.get(metric_id=2), model=model, evaluationdataset=evalset, value=distinct_1(model_responses)),
        AutomaticEvaluation(metric=Metric.objects.get(metric_id=3), model=model, evaluationdataset=evalset, value=distinct_2(model_responses))
    ])