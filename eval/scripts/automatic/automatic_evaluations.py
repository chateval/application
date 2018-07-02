from pymagnitude import Magnitude
from orm.models import AutomaticEvaluation, Metric
from orm.scripts import get_messages, get_baseline_messages
from .auto_eval_utils import avg_len, distinct_1, distinct_2, greedy_match, greedy_score, extrema_score, average_embedding_score

class Word2Vec:
    def __init__(self, vectors):
        self.vectors = vectors
        self.layer1_size = self.vectors.dim
    
    def __getitem__(self, word):
        return self.vectors.query(word)
    
    def __contains__(self, word):
        return word in self.vectors
    
    def dim(self):
        return self.vectors.dim

def run_automatic_evaluation(model, submission, model_responses, evalset):
    model_id = model.model_id
    evalset_id = evalset.pk
    baseline_responses = [message['response'] for message in get_baseline_messages(evalset_id)]

    vectors = Magnitude('eval/scripts/files/google_news.magnitude')
    w2v = Word2Vec(vectors)

    AutomaticEvaluation.objects.bulk_create([
        AutomaticEvaluation(metric=Metric.objects.get(metric_id=1), model=model, evaluationdataset=evalset, value=avg_len(model_responses), model_submission=submission),
        AutomaticEvaluation(metric=Metric.objects.get(metric_id=2), model=model, evaluationdataset=evalset, value=distinct_1(model_responses), model_submission=submission),
        AutomaticEvaluation(metric=Metric.objects.get(metric_id=3), model=model, evaluationdataset=evalset, value=distinct_2(model_responses), model_submission=submission),
        AutomaticEvaluation(metric=Metric.objects.get(metric_id=4), model=model, evaluationdataset=evalset, value=greedy_match(model_responses, baseline_responses, w2v)[0], model_submission=submission),
        AutomaticEvaluation(metric=Metric.objects.get(metric_id=5), model=model, evaluationdataset=evalset, value=extrema_score(model_responses, baseline_responses, w2v)[0], model_submission=submission),
        AutomaticEvaluation(metric=Metric.objects.get(metric_id=6), model=model, evaluationdataset=evalset, value=average_embedding_score(model_responses, baseline_responses, w2v)[0], model_submission=submission),
    ])