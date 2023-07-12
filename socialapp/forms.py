from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser, Question, Answer, ChatTalk, Post, UserGroup
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
    # question = forms.CharField(
    #     max_length=500,
    #     required=True,
    #     label="質問"
    # )

    class Meta:
        model = Question
        fields = ("question",)
        labels = {"question": "質問"}

class AnswerQuestionForm(ModelForm):
    # answer = forms.CharField(
    #     max_length=1000,
    #     required=True,
    #     label="回答"
    # )

    class Meta:
        model = Answer
        fields = ("answer",)
        labels = {"answer": "回答"}

class ChatForm(ModelForm):
    talk = forms.CharField(
        max_length=500,
        required=True,
    )

    class Meta:
        model = ChatTalk
        fields = ("talk",)

class PostForm(ModelForm):
    group_select = forms.MultipleChoiceField(
        label="グループ",
        required=True,
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Post
        fields = ("text", "image1", "group_select")

class PostFilterForm(Form):
    group = forms.MultipleChoiceField(
        label="グループ",
        required=True,
        widget=forms.CheckboxSelectMultiple
    )
    filter = forms.CharField(
        label="",
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "ユーザー名または内容を検索"})
    )
    
class CreateGroupForm(ModelForm):
    name = forms.CharField(
        max_length=50,
        label="グループ名",
    )

    class Meta:
        model = UserGroup
        fields = ["name"]

class RegisterClassesForm(Form):
    jsoncode = forms.CharField(
        label="",
        widget=forms.Textarea()
    )

class RegisterClassesDoneForm(Form):
    classes = forms.MultipleChoiceField(
        label="",
        widget=forms.CheckboxSelectMultiple
    )