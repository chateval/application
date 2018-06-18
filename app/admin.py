from django.contrib import admin
from .models import Baseline, Dataset
from .auto_models import Author, Model, Metric, EvaluationDataset, EvaluationDatasetText, ModelResponse, AutomaticEvaluation, HumanEvaluationsABComparison

admin.site.register(Baseline)
admin.site.register(Dataset)
admin.site.register(Author)
admin.site.register(Model)
admin.site.register(Metric)
admin.site.register(ModelResponse)
admin.site.register(EvaluationDataset)
admin.site.register(EvaluationDatasetText)
admin.site.register(AutomaticEvaluation)
admin.site.register(HumanEvaluationsABComparison)