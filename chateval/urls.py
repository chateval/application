from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from eval.views import uploads, submit, delete, publish, human
from core.views import splash, conversations, model, faq, about
from orm.api import api, responses, evaluationdatasets, prompts, models, automatic_evaluations, baselines, metrics
from accounts.views import login_view, signup_view

urlpatterns = [
    # ACCOUNT ROUTES
    path('admin/', admin.site.urls),
    path('accounts/login/', login_view, name='login'),
    path('accounts/signup/', signup_view, name='signup'),
    path('accounts/', include('django.contrib.auth.urls')),
    # API ROUTES
    path('api/automatic_evaluations', automatic_evaluations, name='automatic_evaluations'),
    path('api/models', models, name='models'),
    path('api/baselines', baselines, name='baselines'),
    path('api/evaluationdatasets', evaluationdatasets, name='evaluationdatasets'),
    path('api/prompts', prompts, name='prompts'),
    path('api/metrics', metrics, name='metrics'),
    path('api/responses', responses, name='responses'),
    path('api/', api, name='api'),
    ### ACTIONS
    path('model/delete/', delete, name='delete'),
    path('model/publish/', publish, name='publish'),
    ## SITE ROUTES
    path('uploads/', uploads, name='uploads'),
    path('model', model, name='model'),
    path('submit', submit, name='submit'),
    path('conversations', conversations, name='conversations'),
    path('faq', faq, name='faq'),
    path('about', about, name='about'),
    path('', splash, name='splash'),
    # EVALUATION
    path('human', human, name="human"),
]