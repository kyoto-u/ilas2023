from django.urls import path, include, re_path
from django.views.static import serve
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('signup', views.signup_view, name='signup_view'),
    path('login', views.Login.as_view(), name='login_view'),
    path('question', views.question, name='question'),
    path('question/ask', views.question_ask, name='question_ask'),
    path('question/answer/<int:question_id>', views.question_answer, name='question_answer'),
    path('user/<int:user_id>', views.user_view, name='user_view'),
    path('chat/<int:user_id>', views.chat, name='chat'),
    path('posts', views.PostsView.as_view(), name='posts_view'),
    path('posts/create', views.PostCreate.as_view(), name='post_create'),
    path('users', views.UsersView.as_view(), name="users_view"),
    path('groups/create', views.CreateGroupView.as_view(), name="create_group"),
    path('groups/join/<int:category>/<int:number>', views.group_join_view, name='group_join'),
    path('groups/leave/<int:category>/<int:number>', views.group_leave_view, name='group_leave'),
    path('groups/posts/<int:category>/<int:number>', views.GroupPostsView.as_view(), name='group_posts'),
    path('groups', views.GroupsView.as_view(), name="groups_view"),
    path('class/register', views.RegisterClasses.as_view(), name="register_classes"),
    path('class/register/done', views.RegisterClassesDone.as_view(), name="register_classes_done"),
    path('logout', views.Logout.as_view(), name="logout_view")
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    urlpatterns.append(re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}))
    urlpatterns.append(re_path(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}))