import datetime
import json


from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import DatabaseError
from django.shortcuts import render, redirect
from django.views import View
from django import http
from django.urls import reverse
from django.conf import settings
from datetime import date

from QAPMS.utils.uploadfile import upload_file
from QAPMS.utils.response_code import RETCODE
from .models import ProjectInformation, ProductInformation, ProjectDocuments, Schedule

# Create your views here.

class Documents(LoginRequiredMixin, View):

    def post(self, request, project_id):
        document_type = request.POST.get('document_type')
        document_desc = request.POST.get('document_desc')
        file = request.FILES.get('file')
        file_name = 'SOW_' + str(date.today()).replace('-', '') + '_' + file.name
        save_path = '%s/documents/%s' % (settings.MEDIA_ROOT, file_name)
        md5 = upload_file(save_path, file)
        count = ProjectDocuments.objects.filter(md5=md5).count()
        if count == 1:
            exit_file = ProjectDocuments.objects.get(md5=md5).file
            return http.JsonResponse({'code': RETCODE.PARAMERR, 'error_msg': '文件已经存在', '文件名': exit_file})
        else:
            try:
                d = ProjectDocuments(project_id=project_id,
                                     document_type=document_type,
                                     document_desc=document_desc,
                                     file='documents/%s' % file_name,
                                     md5=md5)
                d.save()
            except DatabaseError:
                return http.JsonResponse({'code': RETCODE.DBERR, 'error_msg': '存储失败'})
            return redirect(reverse('projects:project', args=(project_id,)))

class ProjectUpdateView(LoginRequiredMixin, View):
    def put(self, request, project_id):
        # 转化axios发送的Json数据
        json_str = request.body.decode()
        project_update = json.loads(json_str)
        projects = ProjectInformation.objects.all()
        # 尝试从数据库根据ID获取项目
        try:
            project = ProjectInformation.objects.get(id=project_id)
        except DatabaseError:
            return http.HttpResponseForbidden('DB error:输入的项目ID错误')
        # 开始与数据库表头匹配关键字，检查字典的Key有哪些
        if 'project_name' in project_update.keys():
            # 检查名称是否重复
            new_name = project_update.get('project_name')
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
                return http.JsonResponse({'code': RETCODE.OK, 'update_name_show': True})
        # 修改项目描述
        if 'project_desc' in project_update.keys():
            new_desc = project_update.get('project_desc')
            try:
                project.project_desc = new_desc
                project.save()
            except DatabaseError:
                return http.HttpResponseForbidden('DB error:输入的项目描述错误')
            return http.JsonResponse({'code': RETCODE.OK, 'update_desc_show': True})
        # 修改项目成员
        if 'project_manager' in project_update.keys():
            # 是否没有输入任何值
            if len(project_update.values()) == 0:
                return http.JsonResponse({'code': RETCODE.PARAMERR, 'update_members_show': False,
                                          'error_update_members_msg': '没有做任何修改'})
            # 有输入值则对非空的key进行数据库更新
            new_pjm = project_update.get('project_manager')
            if new_pjm:
                try:
                    project.project_manager = new_pjm
                    project.save()
                except DatabaseError:
                    return http.HttpResponseForbidden('DB error:输入的项目成员错误')
            new_pdm = project_update.get('product_manager')
            if new_pdm:
                try:
                    project.product_manager = new_pdm
                    project.save()
                except DatabaseError:
                    return http.HttpResponseForbidden('DB error:输入的项目成员错误')
            new_QAPL = project_update.get('QAPL')
            if new_QAPL:
                try:
                    project.QAPL = new_QAPL
                    project.save()
                except DatabaseError:
                    return http.HttpResponseForbidden('DB error:输入的项目成员错误')
            new_EPL = project_update.get('EPL')
            if new_EPL:
                try:
                    project.EPL = new_EPL
                    project.sava()
                except DatabaseError:
                    return http.HttpResponseForbidden('DB error:输入的项目成员错误')
            return http.JsonResponse({'code': RETCODE.OK, 'update_members_show': True})
        # 修改项目计划
        if 'pstart' in project_update.keys():
            new_pstart = project_update.get('pstart')
            new_pend = project_update.get('pend')
            try:
                project.plan_start = new_pstart
                project.plan_end = new_pend
                project.save()
            except DatabaseError:
                return http.HttpResponseForbidden('DB error:输入的项目计划错误')
            return http.JsonResponse({'code': RETCODE.OK, 'new_plan': True})
        # 修改项目实际周期
        if 'practical_start' in project_update.keys():
            new_practical_start = project_update.get('practical_start')
            new_practical_end = project_update.get('practical_end')
            try:
                project.practical_start = new_practical_start
                project.practical_end = new_practical_end
                project.save()
            except DatabaseError:
                return http.HttpResponseForbidden('DB error:输入的项目实际周期错误')
            return http.JsonResponse({'code': RETCODE.OK, 'new_practical': True})
        # 修改项目PG4计划
        PG4_plan = Schedule.objects.get(project_id=project_id, phase=4)
        if 'PG4_pstart' in project_update.keys():
            new_PG4_pstart = project_update.get('PG4_pstart')
            new_PG4_pend = project_update.get('PG4_pend')
            try:
                PG4_plan.plan_start = new_PG4_pstart
                PG4_plan.plan_end = new_PG4_pend
                PG4_plan.save()
            except DatabaseError:
                return http.HttpResponseForbidden('DB error:输入的项目计划错误')
            return http.JsonResponse({'code': RETCODE.OK, 'new_PG4_plan': True})
        # 修改项目PG4实际周期
        if 'PG4_practical_start' in project_update.keys():
            new_practical_start = project_update.get('PG4_practical_start')
            new_practical_end = project_update.get('PG4_practical_end')
            try:
                PG4_plan.practical_start = new_practical_start
                PG4_plan.practical_end = new_practical_end
                PG4_plan.save()
            except DatabaseError:
                return http.HttpResponseForbidden('DB error:输入的项目计划错误')
            return http.JsonResponse({'code': RETCODE.OK, 'new_PG4_plan': True})

class StoriesView(LoginRequiredMixin, View):
    def get(self, request, project_id):
        return render(request, 'stories.html')

class TestView(View):
    def get(self, request):
        return render(request, 'test.html')

    def post(self, request):

        return http.HttpResponse()

class AddProductsView(LoginRequiredMixin, View):
    def get(self, request, project_id):
        return redirect(reverse('projects:project'), args=[project_id])

    def post(self, request, project_id):
        json_str = request.body.decode()
        product_list = json.loads(json_str)
        for product in product_list:
            SKU = product.get('SKU').upper()
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
        return redirect(reverse('projects:project', args=[project_id]))

    def put(self, request, project_id):
        json_str = request.body.decode()
        product_dir = json.loads(json_str)
        SKU_id = product_dir.get('id')
        SKU = product_dir.get('SKU').upper()
        product_type = product_dir.get('product_type')
        SKU_name = product_dir.get('SKU_name')
        SKU_desc = product_dir.get('SKU_desc')
        count = ProductInformation.objects.exclude(id=SKU_id).filter(SKU=SKU).count()
        if count != 0:
            return http.JsonResponse({'code': RETCODE.PARAMERR, 'errmsg': 'SKU重复'})
        try:
            ProductInformation.objects.filter(project=project_id, id=SKU_id).update(
                SKU=SKU,
                product_type=product_type,
                SKU_name=SKU_name,
                SKU_desc=SKU_desc,
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

    def get(self, request, project_id, pg_show='PG1'):
        try:
            project = ProjectInformation.objects.get(id=project_id)
            # 构造项目信息字典返回给前端
            # 将用户地址模型列表转字典列表:因为JsonResponse和Vue.js不认识模型类型，只有Django和Jinja2模板引擎认识
            # 1.构造设备信息
            SKUs = project.productinformation_set.filter(is_delete=False)
            SKU_list = []
            for SKU in SKUs:
                SKU_dir = {
                    'id': SKU.id,
                    'product_type': SKU.get_product_type_display(),
                    'SKU': SKU.SKU,
                    'SKU_name': SKU.SKU_name,
                    'SKU_desc': SKU.SKU_desc,
                }
                SKU_list.append(SKU_dir)

            # 2.构造设备列表
            documents = project.projectdocuments_set.all()
            document_list = []
            for document in documents:
                document_dir = {
                    'id': document.id,
                    'document_type': document.get_document_type_display(),
                    'document_desc': document.document_desc,
                    'file': document.file,
                    'create_time': document.create_time
                }
                document_list.append(document_dir)
            # 3.构造PG时间表
            count1 = Schedule.objects.filter(project=project_id, phase=4).count()
            if count1 == 0:
                pg4_plan_dir = {'plan_start': '', 'plan_end': '', 'practical_start': '', 'practical_end': ''}
            else:
                pg4_plan = Schedule.objects.get(project=project_id, phase=4)
                pg4_plan_dir = {'plan_start': pg4_plan.plan_start or '',
                                'plan_end': pg4_plan.plan_end or '',
                                'practical_start': pg4_plan.practical_start or '',
                                'practical_end': pg4_plan.practical_end or ''}

            count2 = Schedule.objects.filter(project=project_id, phase=5).count()
            if count2 == 0:
                pg5_plan_dir = {'plan_start': '', 'plan_end': '', 'practical_start': '', 'practical_end': ''}
            else:
                pg5_plan = Schedule.objects.get(project=project_id, phase=5)
                pg5_plan_dir = {'plan_start': pg5_plan.plan_start or '',
                                'plan_end': pg5_plan.plan_end or '',
                                'practical_start': pg5_plan.practical_start or '',
                                'practical_end': pg5_plan.practical_end or ''}
            # 4.整合项目信息
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
                'SKUs': SKU_list,
                'PG_show': pg_show,
                'documents': document_list,
                'PG4': pg4_plan_dir,
                'PG5': pg5_plan_dir,
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
            project = ProjectInformation.objects.create(
                project_name=pname, project_desc=pdesc,
                QAPL=QAPL, project_manager=pjm,
                product_manager=pdm, EPL=EPL,
                plan_start=plan_start or datetime.date(2017, 1, 1),
                plan_end=plan_end or datetime.date(2017, 1, 1),
                status=status)
            Schedule.objects.create(project=project.id, phase=4)
            Schedule.objects.create(project=project.id, phase=5)
        except DatabaseError:
            return render(request, 'new_project.html', {'project_code_errmsg': 'create project failed'})
        return redirect(reverse('projects:projects'))

class ProjectCheckView(View):
    def get(self, request, project_name):
        count = ProjectInformation.objects.filter(project_name=project_name).count()
        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': 'OK', 'count': count})
