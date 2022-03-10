from django.shortcuts import render
from django.views import View
from django import http

from QAPMS.utils import response_code
# Create your views here.


class RegisterView(View):

    def get(self, request):
        """
        提供注册界面
        参数：request
        return: 返回注册界面register.html
        """

        return render(request, 'register.html')

    def post(self, request):

        pass