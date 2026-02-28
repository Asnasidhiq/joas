from django.db import models
from django.contrib.auth.models import User

class Question(models.Model):
    text = models.TextField()
    option_a = models.CharField(max_length=200)
    option_b = models.CharField(max_length=200)
    option_c = models.CharField(max_length=200)
    option_d = models.CharField(max_length=200)
    correct_option = models.CharField(max_length=1, choices=[('A','A'),('B','B'),('C','C'),('D','D')])

    def __str__(self):
        return self.text[:50]

class TestResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField()
    total = models.IntegerField()
    date_taken = models.DateTimeField(auto_now_add=True)
    percentage = models.FloatField(default=0.0)
    test_name = models.CharField(max_length=100, default="General Technical Screen")

    def __str__(self):
        return f"{self.user.username} - {self.score}/{self.total}"
