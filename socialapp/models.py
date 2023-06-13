from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    faculty = models.IntegerField(default=0)

class Question(models.Model):
    questioner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    question = models.CharField(max_length=500)

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answerer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    answer = models.CharField(max_length=1000)