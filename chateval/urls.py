from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from eval.views import uploads, submit, confirm_delete
from core.views import splash, conversations, model
from orm.views import archive_model
from accounts.views import login_view, signup_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/login/', login_view, name='login'),
    path('accounts/signup/', signup_view, name='signup'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('evaluation/human', human, name='human'),
    url(r'^uploads$', uploads, name='uploads'),
    path('model/confirm/delete/', confirm_delete, name='confirm_delete'),
    path('model/delete/', archive_model, name='archive_model'),
    url(r'^model$', model, name='model'),
    url(r'^submit$', submit, name='submit'),
    url(r'^conversations$', conversations, name='conversations'),
    url(r'^$', splash, name='splash'),
]