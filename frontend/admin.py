from django.contrib import admin
from .models import SplashBaseline, SplashDataset, Model, Author

admin.site.register(SplashBaseline)
admin.site.register(SplashDataset)
admin.site.register(Author)
admin.site.register(Model)
