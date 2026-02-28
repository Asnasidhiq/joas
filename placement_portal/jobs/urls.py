from django.urls import path
from . import views

urlpatterns = [
    path('', views.job_list, name='job_list'),
    path('upload-csv/', views.upload_jobs_csv, name='upload_jobs_csv'),
    path('sample-csv/', views.download_sample_jobs_csv, name='download_sample_jobs_csv'),
]
