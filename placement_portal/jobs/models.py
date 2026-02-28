from django.db import models

class Job(models.Model):
    title = models.CharField(max_length=200)
    company = models.CharField(max_length=200, default='Unknown')
    description = models.TextField()
    required_qualification = models.CharField(max_length=100)
    interview_date = models.DateTimeField()
    application_link = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} at {self.company}"
