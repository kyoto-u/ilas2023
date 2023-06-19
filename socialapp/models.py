from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    faculty_list = (
        (0, "総合人間学部"),
        (1, "文学部"),
        (2, "教育学部"),
        (3, "法学部"),
        (4, "経済学部"),
        (5, "理学部"),
        (6, "医学部医学科"),
        (7, "医学部人間健康科学科"),
        (8, "薬学部"),
        (9, "工学部"),
        (10, "農学部")
    )
    faculty = models.IntegerField(default=0, choices=faculty_list)

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