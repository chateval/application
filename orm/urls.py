from django.urls import path
from orm.views import (
    welcome,
    human_evaluation,
    ModelList, 
    ModelDetail, 
    BaselineList,
    ModelResponseList, 
    EvaluationDatasetList,
    EvaluationDatasetTextList,
    MetricList,
    AutomaticEvaluationList
)


urlpatterns = [
    path('', welcome),
    path('model', ModelList.as_view(), name='model-list'),
    path('model/<int:pk>', ModelDetail.as_view(), name='model-detail'),
    path('model-response', ModelResponseList.as_view(), name='model-response-list'),
    path('baseline', BaselineList.as_view(), name='baseline-list'),
    path('evaluation-dataset', EvaluationDatasetList.as_view(), name='evaluation-dataset-list'),
    path('evaluation-dataset-text', EvaluationDatasetTextList.as_view(), name='evaluation-dataset-text-list'),
    path('metric', MetricList.as_view(), name='metric-list'),
    path('automatic-evaluation', AutomaticEvaluationList.as_view(), name='automatic-evaluation-list'),
    path('human-evaluation', human_evaluation)
]