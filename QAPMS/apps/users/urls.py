'''定义users app的urls路径'''
from django.urls import path, re_path
from . import views

app_name = 'users'
urlpatterns = [
    # path('', views.LoginView.as_view(), name='login'),
    # index的url路径
    path('index/', views.IndexView.as_view(), name='index'),
    # 用户登录的url路径
    path('login/', views.LoginView.as_view(), name='login'),
    # 用户退出登录的url路径
    path('logout/', views.LogoutView.as_view(), name='logout'),
    # 修改密码的url路径
    path('change_password/(?P<EID>[EH]{1}[0-9]{6})/', views.ChangePassword.as_view(), name='change_password'),
    # 用户注册的url路径
    path('register/',  views.RegisterView.as_view(), name='register'),
    # 判断用户名是否注册
    re_path('username/(?P<username>[a-zA-Z0-9 _-]{5,20})/count/', views.UsernameCountView.as_view()),
    # 判断EID是否注册
    re_path('EID/(?P<EID>[EH]{1}[0-9]{6})/count/', views.EIDCountView.as_view()),
    # 判断EMAIL是否注册
    re_path('email/(?P<email>[a-zA-Z0-9.]+@honeywell.com)/count/', views.EmailCountView.as_view()),
    # 发送邮箱验证码
    re_path('email_codes/(?P<email>[a-zA-Z0-9.]+@honeywell.com)', views.SendEmailCodeView.as_view()),
]
