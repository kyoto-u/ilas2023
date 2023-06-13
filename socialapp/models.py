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

class ChatMessage(models.Model):
    user_from = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="user_from")
    user_to = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="user_to")
    message = models.CharField(max_length=500)
    time = models.DateTimeField(auto_now_add=True)