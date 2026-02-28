from django.contrib import admin
from .models import Job

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'required_qualification', 'interview_date')
    search_fields = ('title', 'company')
    list_filter = ('required_qualification', 'interview_date')
