from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from eval.views import uploads, submit, confirm_delete, human
from core.views import splash, conversations, model, faq
from orm.api import api, responses
from accounts.views import login_view, signup_view


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/login/', login_view, name='login'),
    path('accounts/signup/', signup_view, name='signup'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('api/responses', responses, name='responses'),
    path('api/', api, name='api'),
    path('uploads/', uploads, name='uploads'),
    path('model/confirm/delete/', confirm_delete, name='confirm_delete'),
    path('model', model, name='model'),
    path('submit', submit, name='submit'),
    path('conversations', conversations, name='conversations'),
    path('faq', faq, name='faq'),
    path('', splash, name='splash'),
]