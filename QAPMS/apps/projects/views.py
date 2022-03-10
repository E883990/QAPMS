from django.shortcuts import render
from django.views import View
from django import http
from .models import ProjectInformation
# Create your views here.


class TestView(View):
    def get(self, request):
        return http.HttpResponse('OK!')


class ProjectView(View):
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



class ProjectsView(View):
    def get(self, request):
        # 在.model的ProjectInformation表中条件查询项目数据
        projects = ProjectInformation.objects.all().order_by('id')
        # 将项目模型列表转字典列表:因为JsonResponse和Vue.js不认识模型类型，只有Django和Jinja2模板引擎认识
        if len(projects) == 0:
            return http.HttpResponseForbidden('none proejct exist')
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

        return render(request, 'projects.html', context)

