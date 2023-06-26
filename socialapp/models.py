from typing import Any
from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    faculty_list = (
        (1, "総合人間学部"),
        (2, "文学部"),
        (3, "教育学部"),
        (4, "法学部"),
        (5, "経済学部"),
        (6, "理学部"),
        (7, "医学部医学科"),
        (8, "医学部人間健康科学科"),
        (9, "薬学部"),
        (10, "工学部"),
        (11, "農学部")
    )
    grade_list = (
        (1, "1回生"),
        (2, "2回生"),
        (3, "3回生"),
        (4, "4回生"),
        (5, "5回生"),
        (6, "6回生"),
        # 大学院の指定が面倒なので、今のところは学部生のみ
        # (7, "修士1回生"),
        # (8, "修士2回生"),
        # (9, "博士1回生"),
        # (10, "博士2回生"),
    )

    faculty = models.IntegerField(default=0, choices=faculty_list)
    grade = models.IntegerField(default=1, choices=grade_list) # 年度が変わるごとに更新する必要がある
    image = models.ImageField(default="default.jpg")

class Question(models.Model):
    questioner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    question = models.CharField(max_length=500)
    # 質問した当時の回生・学部学科を保存する
    faculty = models.IntegerField(default=1)
    grade = models.IntegerField(default=1)

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answerer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    answer = models.CharField(max_length=1000)

class ChatTalk(models.Model):
    user_from = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="user_from")
    user_to = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="user_to")
    talk = models.CharField(max_length=500)
    time = models.DateTimeField(auto_now_add=True)