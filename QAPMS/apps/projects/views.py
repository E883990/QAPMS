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
class ProjectUpdateView(LoginRequiredMixin, View):
    def put(self, request, project_id):
        # 转化axios发送的Json数据
        json_str = request.body.decode()
        product_update = json.loads(json_str)
        projects = ProjectInformation.objects.all()
        # 尝试从数据库根据ID获取项目
        try:
            project = ProjectInformation.objects.get(id=project_id)
        except DatabaseError:
            return http.HttpResponseForbidden('输入的项目ID错误')
        # 开始与数据库表头匹配关键字，检查字典的Key有哪些
        if 'project_name' in product_update.keys():
            # 检查名称是否重复
            new_name = product_update.get('project_name')
            name_list = [project.project_name for project in projects]
            if new_name in name_list:
                # 返回错误码给前端展示，
                return http.JsonResponse({'code': RETCODE.PARAMERR, 'error_project_name_msg': True})
            else:
                # 修改数据库
                try:
                    project.project_name = new_name
                    project.save()
                except DatabaseError:
                    return http.HttpResponseForbidden('DB error:输入的项目名称错误')
                return http.JsonResponse({'code': RETCODE.PARAMERR, 'update_name_show': True})
        # 修改项目描述
        if 'project_desc' in product_update.keys():
            new_desc = product_update.get('project_desc')
            try:
                project.project_desc = new_desc
                project.save()
            except DatabaseError:
                return http.HttpResponseForbidden('DB error:输入的项目描述错误')
            return http.JsonResponse({'code': RETCODE.PARAMERR, 'update_desc_show': True})
        # 修改项目成员
        if 'project_manager' in product_update.keys():
            # 是否没有输入任何值
            if len(product_update.values()) == 0:
                return http.JsonResponse({'code': RETCODE.PARAMERR, 'update_members_show': False,
                                          'error_update_members_msg': '没有做任何修改'})
            # 有输入值则对非空的key进行数据库更新
            new_pjm = product_update.get('project_manager')
            if new_pjm:
                try:
                    project.project_manager = new_pjm
                    project.save()
                except DatabaseError:
                    return http.HttpResponseForbidden('DB error:输入的项目成员错误')
            new_pdm = product_update.get('product_manager')
            if new_pdm:
                try:
                    project.product_manager = new_pdm
                    project.save()
                except DatabaseError:
                    return http.HttpResponseForbidden('DB error:输入的项目成员错误')
            new_QAPL = product_update.get('QAPL')
            if new_QAPL:
                try:
                    project.QAPL = new_QAPL
                    project.save()
                except DatabaseError:
                    return http.HttpResponseForbidden('DB error:输入的项目成员错误')
            new_EPL = product_update.get('EPL')
            if new_EPL:
                try:
                    project.EPL = new_EPL
                    project.sava()
                except DatabaseError:
                    return http.HttpResponseForbidden('DB error:输入的项目成员错误')
            return http.JsonResponse({'code': RETCODE.PARAMERR, 'update_members_show': True})


class StoriesView(LoginRequiredMixin, View):
    def get(self, request, project_id):
        return render(request, 'stories.html')

class TestView(View):
    def get(self, request):
        return render(request, 'test.html')

    def post(self, request):
        return http.HttpResponse('收到数据')

class AddProductsView(LoginRequiredMixin, View):
    def get(self, request, project_id):
        pname = ProjectInformation.objects.get(id=project_id).project_name

        return render(request, 'add_product.html', {'pname': pname})

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

    def put(self, request, project_id):
        json_str = request.body.decode()
        product_dir = json.loads(json_str)
        SKU_id = product_dir.get('id')
        SKU = product_dir.get('SKU')
        product_type = product_dir.get('product_type')
        SKU_name = product_dir.get('SKU_name')
        SKU_desc = product_dir.get('SKU_desc')
        count = ProductInformation.objects.exclude(id=SKU_id).filter(SKU=SKU).count()
        if count != 0:
            return http.JsonResponse({'code': RETCODE.PARAMERR, 'errmsg': 'SKU重复'})
        try:
            ProductInformation.objects.filter(id=SKU_id).update(
                SKU=SKU,
                product_type=product_type,
                SKU_name=SKU_name,
                SKU_desc=SKU_desc
            )
        except DatabaseError:
            return http.JsonResponse({'code': RETCODE.DBERR, 'errmsg': '修改SKU失败'})
        # 响应新的地址信息给前端渲染
        new_SKU = ProductInformation.objects.get(id=SKU_id)
        new_SKU_dict = {
            "id": SKU_id,
            "SKU": new_SKU.SKU,
            "product_type": new_SKU.product_type,
            "SKU_name": new_SKU.SKU_name,
            "SKU_desc": new_SKU.SKU_desc,
        }
        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': '修改SKU成功', 'new_product': new_SKU_dict})

class ProjectView(LoginRequiredMixin, View):

    def get(self, request, project_id):
        try:
            project = ProjectInformation.objects.get(id=project_id)
            # 将用户地址模型列表转字典列表:因为JsonResponse和Vue.js不认识模型类型，只有Django和Jinja2模板引擎认识
            SKUs = project.productinformation_set.filter(is_delete=False)
            SKU_list = []
            for SKU in SKUs:
                SKU_dir = {
                    'id': SKU.id,
                    'product_type': SKU.product_type,
                    'SKU': SKU.SKU,
                    'SKU_name': SKU.SKU_name,
                    'SKU_desc': SKU.SKU_desc,
                }
                SKU_list.append(SKU_dir)
            # 构造项目信息字典返回给前端
            project_dir = {
                'project_id': project.id,
                'project_name': project.project_name,
                'project_desc': project.project_desc,
                'QAPL': project.QAPL,
                'project_manager': project.project_manager,
                'EPL': project.EPL,
                'product_manager': project.product_manager,
                'plan_start': project.plan_start,
                'plan_end': project.plan_end,
                'practical_start': project.practical_start or '',
                'practical_end': project.practical_end or '',
                'SKUs': SKU_list
            }
        except DatabaseError:
            return http.HttpResponse('project not found!')
        return render(request, 'project.html', project_dir)


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
                'QAPL': project.QAPL,
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
        return redirect(reverse('projects:addproducts', {{'project_id': project_id}}))


class ProjectCheckView(View):
    def get(self, request, project_name):
        count = ProjectInformation.objects.filter(project_name=project_name).count()
        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': 'OK', 'count': count})
