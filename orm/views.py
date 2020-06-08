from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework.response import Response
from orm.models import (
    Model, 
    ModelResponse,
    EvaluationDataset, 
    EvaluationDatasetText,
    AutomaticEvaluation,  
    HumanEvaluations,
    HumanEvaluationsABComparison
)
from orm.serializers import (
    ModelSerializer, 
    ModelResponseSerializer,
    EvaluationDatasetSerializer, 
    EvaluationDatasetTextSerializer,
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


class ModelResponseList(generics.ListAPIView):
    serializer_class = ModelResponseSerializer

    def get_queryset(self):
        return ModelResponse.objects.filter(
            model=self.request.query_params.get('model_id'),
            evaluationdataset=self.request.query_params.get('evaluationdataset_id')
        )


class EvaluationDatasetList(generics.ListCreateAPIView):
    queryset = EvaluationDataset.objects.all()
    serializer_class = EvaluationDatasetSerializer


class EvaluationDatasetTextList(generics.ListCreateAPIView):
    queryset = EvaluationDatasetText.objects.all()
    serializer_class = EvaluationDatasetTextSerializer

    def get_queryset(self):
        return EvaluationDatasetText.objects.filter(
            evaluationdataset=self.request.query_params.get('evaluationdataset_id'),
        )


class AutomaticEvaluationList(generics.ListAPIView): 
    serializer_class = AutomaticEvaluationSerializer

    def get_queryset(self):
        return AutomaticEvaluation.objects.filter(
            evaluationdataset=self.request.query_params.get('evaluationdataset_id'),
            model=self.request.query_params.get('model_id')
        )


@api_view(['GET'])
def human_evaluation(request, format=None):
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

    return Response({'evaluations': results})