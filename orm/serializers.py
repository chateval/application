from orm.models import Author, Model, EvaluationDataset
from rest_framework import serializers


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['author_id', 'name', 'email', 'institution']


class EvaluationDatasetSerializer(serializers.ModelSerializer):    
    class Meta:
        model = EvaluationDataset
        fields = [
            'evalset_id',
            'name',
            'long_name',
            'source',
            'description',
        ]


class ModelSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()
    evaluationdatasets = EvaluationDatasetSerializer(many=True)

    class Meta:
        model = Model
        fields = [
            'model_id',
            'name',
            'description',
            'author',
            'evaluationdatasets',
            'cp_location',
            'repo_location',
            'comments',
            'public',
            'archived',
            'is_baseline'
        ]