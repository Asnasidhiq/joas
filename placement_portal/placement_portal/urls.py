from django.contrib import admin
from django.urls import path, include
from accounts.views import dashboard

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('allauth.urls')), # Allauth handles login/register/forgot-password/google
    path('jobs/', include('jobs.urls')),
    path('mocktest/', include('mocktest.urls')),
    path('resume/', include('resume_checker.urls')),
    path('', dashboard, name='dashboard'),
]
