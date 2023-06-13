from django.urls import path 
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('signup', views.signup_view, name='signup_view'),
    path('login', views.Login.as_view(), name='login_view'),
    path('question', views.question, name='question'),
    path('question/ask', views.question_ask, name='question_ask'),
    path('question/<int:question_id>', views.question_answer, name='question_answer'),
]