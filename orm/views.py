from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework.response import Response
from orm.models import Model, EvaluationDataset, AutomaticEvaluation
from orm.serializers import (
    ModelSerializer, 
    EvaluationDatasetSerializer, 
    AutomaticEvaluationSerializer
)


@api_view(['GET'])
def welcome(request, format=None):
    return Response({
        'model': reverse('model-list', request=request, format=format),
        'baseline': reverse('baseline-list', request=request, format=format),
        'evaluation-dataset': reverse('evaluation-dataset-list', request=request, format=format),
        'automatic-evaluation': reverse('automatic-evaluation-list', request=request, format=format)
    })


class ModelList(generics.ListCreateAPIView):
    queryset = Model.objects.all()
    serializer_class = ModelSerializer


class ModelDetail(generics.RetrieveAPIView):
    queryset = Model.objects.all()
    serializer_class = ModelSerializer


class BaselineList(generics.ListCreateAPIView):
    queryset = Model.objects.filter(is_baseline=True)
    serializer_class = ModelSerializer


class EvaluationDatasetList(generics.ListCreateAPIView):
    queryset = EvaluationDataset.objects.all()
    serializer_class = EvaluationDatasetSerializer


class AutomaticEvaluationList(generics.ListAPIView): 
    serializer_class = AutomaticEvaluationSerializer

    def get_queryset(self):
        return AutomaticEvaluation.objects.filter(
            evaluationdataset=self.request.query_params.get('evaluationdataset_id'),
            model=self.request.query_params.get('model_id')
        )