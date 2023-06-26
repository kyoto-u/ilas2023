from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser, Question, Answer, ChatTalk
from django.forms import ModelForm, Form

class SignUpForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ("username", "email", "image", "faculty", "grade")
        labels = {"image": "プロフィール画像", "faculty": "学部・学科", "grade": "回生"}

class LoginForm(AuthenticationForm):
    pass

class FilterForm(Form):
    faculty = forms.ChoiceField(choices=((0, "全ての学部"),)+CustomUser.faculty_list, label="学部")
    grade = forms.ChoiceField(choices=((0, "全ての回生"),)+CustomUser.grade_list, label="回生")
    class Meta:
        fields = {"faculty", "grade"}

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
    talk = forms.CharField(
        max_length=500,
        required=True,
    )

    class Meta:
        model = ChatTalk
        fields = ("talk",)