from django.conf.urls import url
from . import views

urlpatterns = [
  url(r'^$', views.splash, name='splash'),
  url(r'^submit$', views.submit, name='submit'),
  url(r'^conversations$', views.conversations, name='conversations')
]