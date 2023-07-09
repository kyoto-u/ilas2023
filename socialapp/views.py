from typing import Any, Dict, Optional, Type
from django.db.models import Q, Max
from django.db.models.query import QuerySet
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404, redirect, render
from .forms import SignUpForm, LoginForm, AskQuestionForm, AnswerQuestionForm, ChatForm, FilterForm, PostForm, PostFilterForm, CreateGroupForm
from .models import CustomUser, Question, Answer, ChatTalk, Post, UserGroup
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import TemplateView, ListView, CreateView
from django.views.generic.edit import FormView
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from urllib.parse import urlencode

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
            user.group.add(UserGroup.objects.get(category=1, number=user.faculty))
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
    if ChatTalk.objects.filter(Q(user_to=request.user) & Q(is_read=False)):
        return render(request, "socialapp/index.html", context={"has_unread": True})
    else:
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
    groups = context["user_obj"].group.exclude((Q(category=0) & Q(number=0)) | (Q(category=3) & Q(number=0)))
    context["groups"] = groups
    return render(request, "socialapp/user.html", context)

@login_required
def chat(request, user_id):
    you = get_object_or_404(CustomUser, id=user_id)
    me = request.user

    form = ChatForm()
    talks_objects = ChatTalk.objects.filter(Q(user_from=me, user_to=you) | Q(user_to=me, user_from=you)).order_by("time")
    talks = [] # [<talkオブジェクト>, <is_read>]の形で格納する
    for talk in talks_objects:
        if (not talk.is_read) and talk.user_to == me:
            talks.append([talk, False])
            talk.is_read = True
            talk.save()
        else:
            talks.append([talk, True])
         
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

class UsersView(LoginRequiredMixin, TemplateView):
    template_name = "socialapp/users.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        me = self.request.user
        category = self.request.GET.get('category')
        number = self.request.GET.get('number')
        users = CustomUser.objects.all().order_by("-date_joined")

        if category and number:
            group = get_object_or_404(UserGroup, category=category, number=number)
            context['group'] = group
            if group in me.group.all():
                context['is_joined'] = True
            else:
                context['is_joined'] = False
            users = users.filter(group=group)

        users_list = [] # [<user>, <has_unread>]
        for user in users:
            if ChatTalk.objects.filter(Q(user_to=me) & Q(user_from=user) & Q(is_read=False)):
                users_list.append([user, True])
            else:
                users_list.append([user, False])
        context['customuser_list'] = users_list
        return context

class GroupsView(LoginRequiredMixin, TemplateView):
    template_name = "socialapp/groups.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['faculty_group'] = UserGroup.objects.filter(category=1)
        context['grade_group'] = UserGroup.objects.filter(category=2)
        context['other_group'] = UserGroup.objects.exclude(Q(category=0) | Q(category=1) | Q(category=2))
        return context
class CreateGroupView(LoginRequiredMixin, CreateView):
    template_name = "socialapp/create_group.html"
    model = UserGroup
    form_class = CreateGroupForm
    success_url = reverse_lazy("groups_view")

    def form_valid(self, form):
        new_group = form.save(commit=False)
        new_group.category = 4
        number_max = UserGroup.objects.filter(category=4).aggregate(Max("number"))["number__max"]
        if number_max:
            new_group.number = number_max + 1
        else:
            new_group.number = 0
        new_group.save()
        self.request.user.group.add(new_group)
        self.request.user.save()
        return super().form_valid(form)

def group_join_view(request, category, number):
    group = get_object_or_404(UserGroup, category=category, number=number)
    request.user.group.add(group)
    request.user.save()
    parameters = urlencode({'category': category, 'number': number})
    return redirect(f'{reverse_lazy("users_view")}?{parameters}')

def group_leave_view(request, category, number):
    group = get_object_or_404(UserGroup, category=category, number=number)
    request.user.group.remove(group)
    request.user.save()
    parameters = urlencode({'category': category, 'number': number})
    return redirect(f'{reverse_lazy("users_view")}?{parameters}')
    
class PostsView(LoginRequiredMixin, ListView):
    model = Post
    template_name = "socialapp/posts.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = PostFilterForm()
        filter = self.request.GET.get('filter')
        group = self.request.GET.getlist('group')
        if filter:       
            form.initial["filter"] = filter
        if group:
            form.initial['group'] = group
        choices = getMyGroupsChoices(self.request.user) # 選択肢の番号は，"category_number"
        choices.pop(0)
        form.fields['group'].choices = choices
        context["form"] = form
        return context

    def get_queryset(self):
        filter = self.request.GET.get('filter')
        if filter:
            posts_query = Post.objects.filter(Q(text__icontains=filter) | Q(user__username__icontains=filter)).order_by("-time")
        else:
            posts_query = Post.objects.order_by("-time")

        groups = self.request.GET.getlist('group')
        if groups:
            count = 0
            for group in groups:
                category = int(group.split(' ')[0])
                number = int(group.split(' ')[1])
                group_obj = UserGroup.objects.get(category=category, number=number)
                if count == 0:
                    posts = posts_query.filter(group=group_obj)
                else:
                    posts = posts | posts_query.filter(group=group_obj)
                count += 1
            posts_query = posts
        return posts_query
    
class PostCreate(LoginRequiredMixin, CreateView):
    model = Post
    template_name = "socialapp/post_create.html"
    form_class = PostForm
    success_url = reverse_lazy("posts_view")

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        choices = getMyGroupsChoices(self.request.user) # 選択肢の番号は，"category_number"
        form.fields['group_select'].choices = choices
        return form
    
    def form_valid(self, form):
        post = form.save(commit=False)
        post.user = self.request.user
        post.save()
        groups = form.cleaned_data["group_select"]
        if "0 0" in groups:
            post.group.add(UserGroup.objects.get(category=0, number=0))
        else:
            for group in groups:
                category = int(group.split(' ')[0])
                number = int(group.split(' ')[1])
                post.group.add(UserGroup.objects.get(category=category, number=number))
        post.save()
        return super().form_valid(form)
    
def getMyGroupsChoices(user):
    choices = []
    for group in user.group.all().order_by('category'):
        choices.append((str(group.category) + " " + str(group.number), group.name))
    return choices

class Logout(LoginRequiredMixin, LogoutView):
    template_name = "socialapp/logout.html"

# 画像の変更　default.jpgは消さないように！