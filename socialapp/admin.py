from django.contrib import admin
from .models import CustomUser, Question, Answer, Post, ChatTalk, UserGroup

admin.site.register(CustomUser)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Post)
admin.site.register(ChatTalk)
admin.site.register(UserGroup)