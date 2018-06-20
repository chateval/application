from django.conf.urls import url
from django.urls import path, include
from . import views

urlpatterns = [
    path('login', views.login_view, name='login'),
    path('signup', views.signup_view, name='signup'),
    path('', include('django.contrib.auth.urls')),
]