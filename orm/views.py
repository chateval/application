from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework.response import Response
from orm.models import Model
from orm.serializers import ModelSerializer


@api_view(['GET'])
def welcome(request, format=None):
    return Response({
        'model': reverse('model-list', request=request, format=format),
        'baseline': reverse('baseline-list', request=request, format=format)
    })


@api_view(['POST'])
def upload(request):
    pass


class ModelList(generics.ListCreateAPIView):
    queryset = Model.objects.all()
    serializer_class = ModelSerializer


class BaselineList(generics.ListCreateAPIView):
    queryset = Model.objects.filter(is_baseline=True)
    serializer_class = ModelSerializer