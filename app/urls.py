from django.conf.urls import url
from . import views
from .forms import SignUpForm

urlpatterns = [
  url(r'^$', views.splash, name='splash'),
  url(r'^models$', views.models, name='models'),
  url(r'^submit$', views.submit, name='submit'),
  url(r'^conversations$', views.conversations, name='conversations'),
  url(r'^accounts/signup', views.signup_view, name='signup'),
  url(r'^accounts/login', views.login_view, name='login'),
]