'''定义users app的urls路径'''
from django.urls import path
from . import views

app_name = 'users'
urlpatterns = [
    # 用户注册的url路径
    path('register/',  views.RegisterView.as_view(), name='register'),
]
