from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect
from django.views import View
from django import http
import logging
import random
import re
from django_redis import get_redis_connection
from django.db import DatabaseError
from django.urls import reverse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.mixins import LoginRequiredMixin

from QAPMS.utils.response_code import RETCODE
from users.models import User
from . import constants
from celery_tasks.email.tasks import send_email_code
# Create your views here.

logger = logging.getLogger('django')
class ChangePassword(LoginRequiredMixin, View):

    def get(self, request, EID):
        return render(request, 'change_password.html')

    def post(self, request, EID):
        old_pwd = request.POST.get('old_pwd')
        user = authenticate(username=EID, password=old_pwd)
        new_pwd = request.POST.get('new_pwd')
        new_pwd2 = request.POST.get('new_pwd2')
        if user is None:
            return render(request, 'change_password.html', {'cpwd_errmsg':'用户密码错误'})
        if new_pwd != new_pwd2:
            return http.HttpResponseForbidden('参数错误')
        User.objects.filter(EID=EID).update(password=make_password(new_pwd))
        return redirect(reverse('users:login'))


class LogoutView(View):
    """退出登录"""

    def get(self, request):
        """实现退出登录逻辑"""
        # 清理session
        logout(request)
        # 退出登录，重定向到登录页
        response = redirect(reverse('users:index'))
        # 退出登录时清除cookie中的username
        response.delete_cookie('username')
        return response

class LoginView(View):

    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        # 接受参数
        username = request.POST.get('username')
        password = request.POST.get('password')
        remembered = request.POST.get('remembered')

        # 判断参数是否齐全
        if not all([username, password]):
            return http.HttpResponseForbidden('缺少必传参数')


        # 认证登录用户
        user = authenticate(username=username, password=password)
        if user is None:
            return render(request, 'login.html', {'account_errmsg': '用户名或密码错误'})
        # if password
        # 实现状态保持
        login(request, user)
        # 设置状态保持的周期
        if remembered != 'on':
            # 没有记住用户：浏览器会话结束就过期
            request.session.set_expiry(0)
        else:
            # 记住用户：None表示两周后过期
            request.session.set_expiry(None)
        # 响应登录结果
        next = request.GET.get('next')
        if next:
            response = redirect(next)
        else:
            response = redirect(reverse('users:index'))
        # 注册时用户名写入到cookie，有效期15天
        response.set_cookie('username', user.username.replace(' ',''), max_age=3600 * 24 * 15)
        response.set_cookie('EID', user.EID, max_age=3600 * 24 * 15)
        # 响应登录结果
        return response

class IndexView(View):

    def get(self, request):
        return render(request, 'index.html')

class SendEmailCodeView(View):
    """发送验证码"""

    def get(self, request, email):
        """
        :param request: 请求对象
        :param email: 邮箱
        :return: JSON
        """
        # 生成验证码：生成6位数验证码
        if not re.match(r'^[a-zA-Z0-9.]+@honeywell.com$', email):
            return http.HttpResponseForbidden('参数email有误')
        email_code = '%06d' % random.randint(0, 999999)
        logger.info(email_code)
        # 创建连接到redis的对象
        redis_conn = get_redis_connection('verify_code')
        # 判断用户是否频繁发送短信验证码
        send_flag = redis_conn.get('send_flag_%s' % email)
        if send_flag:
            return http.JsonResponse({'code': RETCODE.THROTTLINGERR, 'errmsg': '发送验证码过于频繁'})
        # 创建redis管道
        pl = redis_conn.pipeline()
        # 将命令添加到队列中
        # 保存短信验证码
        pl.setex('email_%s' % email, constants.Email_CODE_REDIS_EXPIRES, email_code)
        # 保存发送短信验证码的标记
        pl.setex('send_flag_%s' % email, constants.SEND_Email_CODE_INTERVAL, 1)
        # 执行
        pl.execute()
        # 发送email
        send_email_code.delay(email, email_code)
        # send_mail('邮箱验证码', '您好，您的邮箱验证码是：'+str(email_code), settings.EMAIL_FROM, [email])
        # print(settings.EMAIL_FROM)
        # 响应结果
        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': 'send success'})

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
        :param: 用户名
        :return: JSON
        """
        # 实现主体业务逻辑：使用EID查询对应的记录的条数(filter返回的是满足条件的结果集)
        count = User.objects.filter(EID=EID).count()
        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': 'OK', 'count': count})


class EmailCountView(View):
    """判断EID是否重复注册"""
    def get(self, request, email):
        """
        :param: 用户名
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
        email_code_client = request.POST.get('email_code')
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
        # 判断邮箱注册码
        redis_conn = get_redis_connection('verify_code')
        email_code_server = redis_conn.get('email_%s' % email)
        if email_code_server is None:
            return render(request, 'register.html', {'email_code_errmsg': '无效的邮箱验证码'})
        if email_code_client != email_code_server.decode():
            return render(request, 'register.html', {'email_code_errmsg': '输入的邮箱验证码有误'})
        # 保存注册数据：是注册业务的核心
        try:
            user = User.objects.create_user(username=username, password=password, email=email, EID=EID)
        except DatabaseError:
            return render(request, 'register.html', {'register_errmsg': '注册失败'})

        # 实现状态保持
        login(request, user)
        # 响应注册结果
        response = redirect(reverse('users:index'))
        # 注册时用户名写入到cookie，有效期15天
        response.set_cookie('username', user.username.replace(' ',''), max_age=3600 * 24 * 15)
        response.set_cookie('EID', user.EID, max_age=3600 * 24 * 15)
        # 响应结果：重定向到首页
        # return http.HttpResponse('注册成功，重定向到首页')
        # return redirect('/')
        # reverse('contents:index') == '/'
        return response

