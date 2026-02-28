from django.urls import path
from . import views

urlpatterns = [
    path('', views.check_resume, name='check_resume'),
]
