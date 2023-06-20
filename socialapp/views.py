from typing import Any
from django.db.models.query import QuerySet
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from .forms import SignUpForm, LoginForm, AskQuestionForm, AnswerQuestionForm, ChatForm, FilterForm
from .models import CustomUser, Question, Answer, ChatMessage
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import TemplateView, ListView
from django.views.generic.edit import FormView
from django.contrib.auth import login, authenticate
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q

def signup_view(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=password) # 認証バックエンド属性を持ったUserを返す
            if user != None:
                login(request, user)
            return redirect("/")
        else:
            print(form.errors)
    else:
        form = SignUpForm()
    return render(request, "socialapp/signup.html", {"form": form})

class Login(LoginView):
    authentication_form = LoginForm
    template_name = "socialapp/login.html"

@login_required
def index(request):
    return render(request, "socialapp/index.html")

@login_required
def question(request, faculty, grade):
    if request.method == "POST":
        faculty_filter = request.POST["faculty"]
        grade_filter = request.POST["grade"]
        return redirect("question", faculty_filter, grade_filter)
    else:
        if faculty == 0 and grade == 0:
            questions = Question.objects.all()
        elif faculty == 0:
            questions = Question.objects.filter(grade=grade)
        elif grade == 0:
            questions = Question.objects.filter(faculty=faculty)
        else:
            questions = Question.objects.filter(grade=grade, faculty=faculty)

        question_list = []
        for question in questions:
            answers = Answer.objects.filter(question=question).all() # ！時間で並び替えるようにする
            question_list.append([question, answers])
        context = {
            "form": FilterForm(initial={"faculty": faculty, "grade": grade}),
            "question_list": question_list,
        }
    return render(request, "socialapp/question.html", context)

@login_required
def question_ask(request):
    user = request.user
    form = AskQuestionForm()
    context = {
        "form": form,
    }
    if request.method == "POST":
        form = AskQuestionForm(request.POST, instance=Question(questioner=user, faculty=user.faculty, grade=user.grade))
        if form.is_valid():
            form.save()
            return redirect("question")
        else:
            print(form.errors)
    return render(request, "socialapp/question_ask.html", context)

@login_required
def question_answer(request, question_id):
    form = AnswerQuestionForm()
    user = request.user
    question = get_object_or_404(Question, id=question_id)
    if request.method == "POST":
        form = AnswerQuestionForm(request.POST, instance=Answer(question=question, answerer=user))
        if form.is_valid():
            form.save()
            return redirect("question")
        else:
            print(form.errors)
    context = {
        "form": form,
        "question": question
    }
    return render(request, "socialapp/question_answer.html", context)

@login_required
def user_view(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    context = {
        "user": user
    }
    if user == request.user:
        context["user_is_me"] = True
    else:
        context["user_is_me"] = False

    return render(request, "socialapp/user.html", context)

@login_required
def chat(request, user_id):
    you = get_object_or_404(CustomUser, id=user_id)
    me = request.user

    form = ChatForm()
    messages = ChatMessage.objects.filter(Q(user_from=me, user_to=you) | Q(user_to=me, user_from=you)).order_by("time")

    if request.method == "POST":
        form = ChatForm(request.POST, instance=ChatMessage(user_from=me, user_to=you))
        if form.is_valid():
            form.save()
            return redirect("chat", you.id)
        else:
            print(form.errors)

    context = {
        "you": you,
        "me": me,
        "messages": messages,
        "form": form,
    }
    return render(request, "socialapp/chat.html", context)

class UsersView(LoginRequiredMixin, ListView):
    model = CustomUser
    template_name = "socialapp/users.html"

    def get_queryset(self):
        users = CustomUser.objects.all().order_by("-date_joined")
        return users
    
class Logout(LoginRequiredMixin, TemplateView):
    template_name = "socialapp/logout.html"