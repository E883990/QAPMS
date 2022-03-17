import datetime
import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import DatabaseError
from django.shortcuts import render, redirect
from django.views import View
from django import http
from django.urls import reverse

from QAPMS.utils.response_code import RETCODE
from .models import ProjectInformation, ProductInformation


# Create your views here.

class TestView(View):
    def get(self, request):
        return render(request, 'test.html')

    def post(self, request):
        return http.HttpResponse('收到数据')

class AddProductsView(View):
    def get(self, request, project_id):
        return render(request, 'add_product.html')

    def post(self, request, project_id):
        json_str = request.body.decode()
        product_list = json.loads(json_str)
        for product in product_list:
            SKU = product.get('SKU')
            SKU_type = product.get('SKU_type')
            SKU_name = product.get('SKU_name')
            SKU_desc = product.get('SKU_desc')
            count = ProductInformation.objects.filter(SKU=SKU).count()
            if count != 0:
                return http.HttpResponseForbidden('product already exist')
            try:
                ProductInformation.objects.create(project_id=project_id, SKU=SKU,
                                                  SKU_name=SKU_name, product_type=SKU_type,
                                                  SKU_desc=SKU_desc)
            except DatabaseError:
                return http.HttpResponse('product save failed!')
        return redirect(reverse('projects:projects'))

class ProjectView(LoginRequiredMixin, View):

    def get(self, request, project_id):
        try:
            project = ProjectInformation.objects.get(id=project_id)
            project_dir = {
                'id': project.id,
                'project_name': project.project_name,
                'project_desc': project.project_desc,
                'QAPL': project.QAPL,
                'project_manager': project.project_manager,
                'product_manager': project.product_manager,
                'EPL': project.EPL,
            }
            context = {'project': project_dir}
            return render(request, 'project.html', context)
        except:
            return http.HttpResponse('project not found!')


class ProjectsView(LoginRequiredMixin, View):

    def get(self, request):
        # 在.model的ProjectInformation表中条件查询项目数据
        projects = ProjectInformation.objects.all().order_by('id')
        # 将项目模型列表转字典列表:因为JsonResponse和Vue.js不认识模型类型，只有Django和Jinja2模板引擎认识
        if len(projects) == 0:
            return http.HttpResponseForbidden('none project exist')
        project_list = []
        for project in projects:
            SKUs = project.productinformation_set.all()
            project_dict = {
                'id': project.id,
                'project_name': project.project_name,
                'project_desc': project.project_desc,
                'QAPL':project.QAPL,
                'project_manager': project.project_manager,
                'EPL': project.EPL,
                'product_manager': project.product_manager,
                'plan_start': project.plan_start,
                'plan_end': project.plan_end,
                'practical_start': project.practical_start,
                'practical_end': project.practical_end,
                'status': project.status,
                'SKUs': SKUs
            }
            project_list.append(project_dict)
        # 构造上下文
        context = {
            'projects': project_list
        }
        return render(request, 'projects.html', context=context)

class CreateProjectView(LoginRequiredMixin, View):

    def get(self, request):
        return render(request, 'new_project.html')

    def post(self, request):
        pname = request.POST.get('pname')
        pdesc = request.POST.get('pdesc')
        pjm = request.POST.get('pjm')
        pdm = request.POST.get('pdm')
        QAPL = request.POST.get('QAPL')
        EPL = request.POST.get('EPL')
        plan_start = request.POST.get('pstart')
        plan_end = request.POST.get('pend')
        count = ProjectInformation.objects.filter(project_name=pname).count()

        if count != 0:
            return http.HttpResponseForbidden('项目已存在')
        if QAPL:
            if plan_start:
                status = 3
            else:
                status = 2
        else:
            status = 1
        try:
            ProjectInformation.objects.create(project_name=pname, project_desc=pdesc,
                                              QAPL=QAPL, project_manager=pjm,
                                              product_manager=pdm, EPL=EPL,
                                              plan_start=plan_start or datetime.date(2017, 1, 1),
                                              plan_end=plan_end or datetime.date(2017, 1, 1),
                                              status=status)
        except DatabaseError:
            return render(request, 'new_project.html', {'project_code_errmsg': 'create project failed'})
        project_id = ProjectInformation.objects.get(project_name=pname).id
        return redirect(reverse('projects:addproducts', kwargs={'project_id': project_id}))


class ProjectCheckView(View):
    def get(self, request, project_name):
        count = ProjectInformation.objects.filter(project_name=project_name).count()
        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': 'OK', 'count': count})
