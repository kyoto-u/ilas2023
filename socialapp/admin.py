from django.contrib import admin
from .models import CustomUser, Question, Answer, Post

admin.site.register(CustomUser)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Post)