from django.contrib import admin
from .models import AutomaticEvaluation, Baseline, Author, Model, Metric, EvaluationDataset, EvaluationDatasetText, ModelResponse, ModelSubmission, HumanEvaluationsABComparison

admin.site.register(Baseline)
admin.site.register(EvaluationDataset)
admin.site.register(EvaluationDatasetText)
admin.site.register(Author)
admin.site.register(Model)
admin.site.register(ModelResponse)
admin.site.register(ModelSubmission)
admin.site.register(Metric)
admin.site.register(HumanEvaluationsABComparison)
admin.site.register(AutomaticEvaluation)
