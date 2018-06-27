from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from eval.views import my_models, models
from core.views import splash, submit, conversations
from accounts.views import login_view, signup_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login', login_view, name='login'),
    path('signup', signup_view, name='signup'),
    path('', include('django.contrib.auth.urls')),
    url(r'evaluation^$', my_models, name='my_models'),
    url(r'^evaluation/models$', models, name='models'),
    url(r'^$', splash, name='splash'),
    url(r'^submit$', submit, name='submit'),
    url(r'^conversations$', conversations, name='conversations')
]