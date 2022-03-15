from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import DatabaseError
from django.shortcuts import render, redirect
from django.views import View
from django import http
from django.urls import reverse

from QAPMS.utils.response_code import RETCODE
from .models import ProjectInformation
# Create your views here.


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
            project_dict = {
                'id': project.id,
                'project_name': project.project_name,
                'project_desc': project.project_desc,
            }
            project_list.append(project_dict)
        # 构造上下文
        context = {
            # 'default_project_id': login_user.default_address_id or '0',
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
        status = request.POST.get('PG')
        count = ProjectInformation.objects.filter(project_name=pname).count()
        if count != 0:
            return http.HttpResponseForbidden('项目已存在')
        try:
            ProjectInformation.objects.create(project_name=pname, project_desc=pdesc,
                                              QAPL=QAPL, project_manager=pjm,
                                              product_manager=pdm, EPL=EPL,
                                              plan_start=plan_start, plan_end=plan_end,
                                              status=status)
        except DatabaseError:
            return render(request, 'new_project.html', {'new_project_errmsg': '注册失败'})
        return redirect(reverse('projects:projects'))

class ProjectCheckView(View):
    def get(self, request, project_name):
        count = ProjectInformation.objects.filter(project_name=project_name).count()
        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': 'OK', 'count': count})
