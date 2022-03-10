from django.shortcuts import render, redirect
from django.views import View
from django import http
import re
from django.db import DatabaseError
from django.urls import reverse
from django.contrib.auth import login

from QAPMS.utils.response_code import RETCODE
from users.models import User
# Create your views here.


class UsernameCountView(View):
    """判断用户名是否重复注册"""
    def get(self, request, username):
        """
        :param username: 用户名
        :return: JSON
        """
        # 实现主体业务逻辑：使用username查询对应的记录的条数(filter返回的是满足条件的结果集)
        count = User.objects.filter(username=username).count()
        # 响应结果
        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': 'OK', 'count': count})


class EIDCountView(View):
    """判断EID是否重复注册"""

    def get(self, request, EID):
        """
        :param username: 用户名
        :return: JSON
        """
        # 实现主体业务逻辑：使用EID查询对应的记录的条数(filter返回的是满足条件的结果集)
        count = User.objects.filter(EID=EID).count()
        # 响应结果
        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': 'OK', 'count': count})


class EmailCountView(View):
    """判断EID是否重复注册"""
    def get(self, request, email):
        """
        :param username: 用户名
        :return: JSON
        """
        # 实现主体业务逻辑：使用EID查询对应的记录的条数(filter返回的是满足条件的结果集)
        count = User.objects.filter(email=email).count()
        # 响应结果
        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': 'OK', 'count': count})


class RegisterView(View):

    def get(self, request):
        """
        提供注册界面
        参数：request
        return: 返回注册界面register.html
        """
        return render(request, 'register.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        email = request.POST.get('email')
        EID = request.POST.get('EID')
        # 校验参数：前后端的校验需要分开，避免恶意用户越过前端逻辑发请求，要保证后端的安全，前后端的校验逻辑相同
        # 判断参数是否齐全:all([列表])：会去校验列表中的元素是否为空，只要有一个为空，返回false
        if not all([username, password, password2, email, EID]):
            return http.HttpResponseForbidden('缺少必传参数')
        # 判断用户名是否是5-20个字符
        if not re.match(r'^[a-zA-Z0-9 _-]{5,20}$', username):
            return http.HttpResponseForbidden('请输入5-20个字符的用户名')
        # 判断密码是否是8-20个数字
        if not re.match(r'^[0-9A-Za-z\W]{8,20}$', password):
            return http.HttpResponseForbidden('请输入8-20位的密码')
        # 判断两次密码是否一致
        if password != password2:
            return http.HttpResponseForbidden('两次输入的密码不一致')
        # 判断email是否合法
        if not re.match(r'^[0-9a-zA-Z.]+@honeywell.com$', email):
            return http.HttpResponseForbidden('请输入正确的email')
        # 判断EID是否合法
        if not re.match(r'^[EH]{1}[0-9]{6}$', EID):
            return http.HttpResponseForbidden('请输入正确的EID')
        # 判断账户是否已经存在
        count = User.objects.filter(username=username).count() + User.objects.filter(
            EID=EID).count() + User.objects.filter(email=email).count()
        if count != 0:
            return http.HttpResponseForbidden('账号/EID/邮箱已存在')

        # 保存注册数据：是注册业务的核心
        # return render(request, 'register.html', {'register_errmsg': '注册失败'})
        try:
            user = User.objects.create_user(username=username, password=password, email=email, EID=EID)
        except DatabaseError:
            return render(request, 'register.html', {'register_errmsg': '注册失败'})

        # 实现状态保持
        login(request, user)

        # 响应结果：重定向到首页
        # return http.HttpResponse('注册成功，重定向到首页')
        # return redirect('/')
        # reverse('contents:index') == '/'
        return redirect(reverse('contents:index'))