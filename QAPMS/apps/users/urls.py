'''定义users app的urls路径'''
from django.urls import path, re_path
from . import views

app_name = 'users'
urlpatterns = [
    # 用户注册的url路径
    path('register/',  views.RegisterView.as_view(), name='register'),
    # 判断用户名是否注册
    re_path('username/(?P<username>[a-zA-Z0-9 _-]{5,20})/count/', views.UsernameCountView.as_view()),
    # 判断EID是否注册
    re_path('EID/(?P<EID>[EH]{1}[0-9]{6})/count/', views.EIDCountView.as_view()),
    # 判断EMAIL是否注册
    re_path('email/(?P<email>[a-zA-Z0-9.]+@honeywell.com)/count/', views.EmailCountView.as_view()),
]
