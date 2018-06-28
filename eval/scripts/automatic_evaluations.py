from gensim.models import KeyedVectors
from orm.models import AutomaticEvaluation, Metric
from orm.scripts import get_messages, get_baseline_messages
from .auto_eval_utils import avg_len, distinct_1, distinct_2, greedy_match, greedy_score, extrema_score, average_embedding_score

def run_automatic_evaluation(model, evalset):
    model_id = model.model_id
    evalset_id = evalset.pk
    model_responses = [message['response'] for message in get_messages(model_id, evalset_id)]
    baseline_responses = [message['response'] for message in get_baseline_messages(evalset_id)]

    w2v = KeyedVectors.load_word2vec_format("eval/scripts/files/google_news_vectors.gz", binary=True)

    AutomaticEvaluation.objects.bulk_create([
        AutomaticEvaluation(metric=Metric.objects.get(metric_id=1), model=model, evaluationdataset=evalset, value=avg_len(model_responses)),
        AutomaticEvaluation(metric=Metric.objects.get(metric_id=2), model=model, evaluationdataset=evalset, value=distinct_1(model_responses)),
        AutomaticEvaluation(metric=Metric.objects.get(metric_id=3), model=model, evaluationdataset=evalset, value=distinct_2(model_responses)),
        AutomaticEvaluation(metric=Metric.objects.get(metric_id=4), model=model, evaluationdataset=evalset, value=greedy_match(model_responses, baseline_responses, w2v)[0]),
        AutomaticEvaluation(metric=Metric.objects.get(metric_id=6), model=model, evaluationdataset=evalset, value=extrema_score(model_responses, baseline_responses, w2v)[0]),
        AutomaticEvaluation(metric=Metric.objects.get(metric_id=7), model=model, evaluationdataset=evalset, value=average_embedding_score(model_responses, baseline_responses, w2v)[0]),
    ])