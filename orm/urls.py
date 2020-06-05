from django.urls import path
from orm.views import (
    welcome, 
    ModelList, 
    ModelDetail, 
    BaselineList, 
    EvaluationDatasetList,
    AutomaticEvaluationList
)


urlpatterns = [
    path('', welcome),
    path('model', ModelList.as_view(), name='model-list'),
    path('model/<int:pk>', ModelDetail.as_view(), name='model-detail'),
    path('baseline', BaselineList.as_view(), name='baseline-list'),
    path('evaluation-dataset', EvaluationDatasetList.as_view(), name='evaluation-dataset-list'),
    path('automatic-evaluation', AutomaticEvaluationList.as_view(), name='automatic-evaluation-list'),
]