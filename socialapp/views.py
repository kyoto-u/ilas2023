from typing import Any, Dict
from django.db.models import Q
from django.db.models.query import QuerySet
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404, redirect, render
from .forms import SignUpForm, LoginForm, AskQuestionForm, AnswerQuestionForm, ChatForm, FilterForm, PostForm, PostFilterForm
from .models import CustomUser, Question, Answer, ChatTalk, Post
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import TemplateView, ListView, CreateView
from django.views.generic.edit import FormView
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q

def signup_view(request):
    if request.method == "POST":
        form = SignUpForm(request.POST, request.FILES)
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
    if request.method == "POST":
        request.user.question_faculty_filter = request.POST["faculty"]
        request.user.question_grade_filter = request.POST["grade"]
        request.user.save()
        return redirect("question")
    else:
        faculty = request.user.question_faculty_filter
        grade = request.user.question_grade_filter
        if faculty == 0 and grade == 0:
            questions = Question.objects.all()
        elif faculty == 0:
            questions = Question.objects.filter(grade=grade)
        elif grade == 0:
            questions = Question.objects.filter(faculty=faculty)
        else:
            questions = Question.objects.filter(grade=grade, faculty=faculty)

        questions = questions.order_by("-time")
        question_list = []
        for question in questions:
            answers = Answer.objects.filter(question=question).order_by("-time")
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
    context = {
        "user_obj": get_object_or_404(CustomUser, id=user_id)
    }
    return render(request, "socialapp/user.html", context)

@login_required
def chat(request, user_id):
    you = get_object_or_404(CustomUser, id=user_id)
    me = request.user

    form = ChatForm()
    talks = ChatTalk.objects.filter(Q(user_from=me, user_to=you) | Q(user_to=me, user_from=you)).order_by("time")

    if request.method == "POST":
        form = ChatForm(request.POST, instance=ChatTalk(user_from=me, user_to=you))
        if form.is_valid():
            form.save()
            return redirect("chat", you.id)
        else:
            print(form.errors)

    context = {
        "you": you,
        "me": me,
        "talks": talks,
        "form": form,
    }
    return render(request, "socialapp/chat.html", context)

class UsersView(LoginRequiredMixin, ListView):
    model = CustomUser
    template_name = "socialapp/users.html"

    def get_queryset(self):
        users = CustomUser.objects.all().order_by("-date_joined")
        return users
    
class PostsView(LoginRequiredMixin, ListView):
    model = Post
    template_name = "socialapp/posts.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        filter = self.request.GET.get('filter')
        if filter:
            context["form"] = PostFilterForm(initial={"filter": filter})
        else:
            context["form"] = PostFilterForm()
        return context

    def get_queryset(self):
        filter = self.request.GET.get('filter')
        if filter:
            posts = Post.objects.filter(Q(text__icontains=filter) | Q(user__username__icontains=filter)).order_by("-time")
        else:
            posts = Post.objects.order_by("-time")
        return posts
    
class PostCreate(LoginRequiredMixin, CreateView):
    model = Post
    template_name = "socialapp/post_create.html"
    form_class = PostForm
    success_url = reverse_lazy("posts_view")

    def form_valid(self, form):
        post = form.save(commit=False)
        post.user = self.request.user
        post.save()
        return super().form_valid(form)

    
class Logout(LoginRequiredMixin, LogoutView):
    template_name = "socialapp/logout.html"

# 画像の変更　default.jpgは消さないように！