from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from .forms import SignUpForm, LoginForm, AskQuestionForm, AnswerQuestionForm
from .models import Question, Answer
from django.contrib.auth.views import LoginView
from django.views.generic.edit import FormView
from django.contrib.auth import login, authenticate
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

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
def question(request):
    questions = Question.objects.all()
    question_list = []
    for question in questions:
        answers = Answer.objects.filter(question=question).all() # ！時間で並び替えるようにする
        question_list.append([question, answers])
    context = {
        "question_list": question_list
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
        form = AskQuestionForm(request.POST, instance=Question(questioner=user))
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
