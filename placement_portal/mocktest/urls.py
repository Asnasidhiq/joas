from django.urls import path
from . import views

urlpatterns = [
    path('', views.take_test, name='take_test'),
    path('results/', views.test_result, name='test_result'),
    path('upload-csv/', views.upload_questions_csv, name='upload_questions_csv'),
    path('sample-csv/', views.download_sample_questions_csv, name='download_sample_questions_csv'),
]
