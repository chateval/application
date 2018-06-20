from django.contrib import admin
from .models import Baseline, Dataset, Author, Model

admin.site.register(Baseline)
admin.site.register(Dataset)
admin.site.register(Author)
admin.site.register(Model)