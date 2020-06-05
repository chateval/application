from orm.models import Author, Model, EvaluationDataset, AutomaticEvaluation, ModelSubmission
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


class ModelSubmissionSerializer(serializers.ModelSerializer):
    model = ModelSerializer()
    evaluationdatasets = EvaluationDatasetSerializer(many=True)

    class Meta:
        model = ModelSubmission
        fields = ['submission_id', 'date', 'model', 'evaluationdatasets']


class AutomaticEvaluationSerializer(serializers.ModelSerializer):
    model = ModelSerializer()
    evaluationdataset = EvaluationDatasetSerializer()
    model_submission = ModelSubmissionSerializer()

    class Meta:
        model = AutomaticEvaluation
        fields = [
            'id',
            'model',
            'metric',
            'evaluationdataset',
            'value',
            'model_submission'
        ]