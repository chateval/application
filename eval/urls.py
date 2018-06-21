from django.conf.urls import url
from . import views

urlpatterns = [
  url(r'^$', views.my_models, name='my_models'),
]