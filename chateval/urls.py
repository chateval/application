from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path
from django.conf.urls import url, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    url(r'', include('core.urls')),    
]