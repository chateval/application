from django.urls import path
from orm.views import welcome, ModelList, BaselineList, EvaluationDatasetList


urlpatterns = [
    path('', welcome),
    path('model', ModelList.as_view(), name='model-list'),
    path('baseline', BaselineList.as_view(), name='baseline-list'),
    path('evaluation-dataset', EvaluationDatasetList.as_view(), name='evaluation-dataset-list')
]