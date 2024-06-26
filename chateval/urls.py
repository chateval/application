from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from eval.views import uploads, submit, delete, publish, human, login_view, signup_view, compare, dbdc5download, dstc10download, dstc11download, dbdc5submit, dstc10submit, dstc11submit, gemv3submit
#from orm.api import api, responses, evaluationdatasets, prompts, models, automatic_evaluations, human_evaluations, baselines, metrics, model as api_model


urlpatterns = [
    # ACCOUNT ROUTES
    path('admin/', admin.site.urls),
    path('accounts/login/', login_view, name='login'),
    path('accounts/signup/', signup_view, name='signup'),
    path('accounts/', include('django.contrib.auth.urls')),
    # API ROUTES
    path('api/', include('orm.urls')),
    ### ACTIONS
    path('model/delete/', delete, name='delete'),
    path('model/publish/', publish, name='publish'),
    path('dbdc5_data/', dbdc5download, name='dbdc5download'),
    path('dstc10_data/', dstc10download, name='dstc10download'),
    path('dstc11_data/', dstc11download, name='dstc11download'),
    ## SITE ROUTES
    path('uploads/', uploads, name='uploads'),
    path('upload', submit, name='submit'),
    path('dbdc5submit/', dbdc5submit, name='dbdc5submit'),
    path('dbdc5submit', dbdc5submit, name='dbdc5submit'),
    path('dstc10submit/', dstc10submit, name='dstc10submit'),
    path('dstc10submit', dstc10submit, name='dstc10submit'), 
    path('dstc11submit/', dstc11submit, name='dstc11submit'),
    path('dstc11submit', dstc11submit, name='dstc11submit'),   
    path('gemv3submit/', gemv3submit, name='gemv3submit'),
    path('gemv3submit', gemv3submit, name='gemv3submit'),   
    
    # EVALUATION
    path('compare', compare, name="compare"),
    path('human', human, name="human"),
    path('', uploads, name="uploads")
]
