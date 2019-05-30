from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from eval.views import uploads, submit, delete, publish, human, login_view, signup_view, compare
from orm.api import api, responses, evaluationdatasets, prompts, models, automatic_evaluations, human_evaluations, baselines, metrics, model as api_model


urlpatterns = [
    # ACCOUNT ROUTES
    path('admin/', admin.site.urls),
    path('accounts/login/', login_view, name='login'),
    path('accounts/signup/', signup_view, name='signup'),
    path('accounts/', include('django.contrib.auth.urls')),
    # API ROUTES
    path('api/automatic_evaluations', automatic_evaluations, name='automatic_evaluations'),
    path('api/human_evaluations', human_evaluations, name='human_evaluations'),
    path('api/models', models, name='models'),
    path('api/model', api_model, name='model'),
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
    path('upload', submit, name='submit'),
    # EVALUATION
    path('compare', compare, name="compare"),
    path('human', human, name="human"),
    path('', uploads, name="uploads")
]
