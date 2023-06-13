from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser, Question, Answer, ChatMessage
from django.forms import ModelForm

class SignUpForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ("username",)

class LoginForm(AuthenticationForm):
    pass

class AskQuestionForm(ModelForm):
    question = forms.CharField(
        max_length=500,
        required=True,
        label="質問"
    )

    class Meta:
        model = Question
        fields = ("question",)

class AnswerQuestionForm(ModelForm):
    answer = forms.CharField(
        max_length=1000,
        required=True,
        label="回答"
    )

    class Meta:
        model = Answer
        fields = ("answer",)

class ChatForm(ModelForm):
    message = forms.CharField(
        max_length=500,
        required=True,
    )

    class Meta:
        model = ChatMessage
        fields = ("message",)