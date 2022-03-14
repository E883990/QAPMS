from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View
from django import http
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



class ProjectsView(LoginRequiredMixin,View):

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

        return render(request, 'projects.html')

class CreateProjectView(LoginRequiredMixin,View):

     def get(self,request):
         return render(request, 'new_project.html')

     def post(self,request):
        pname=request.POST.get('pname')
        pdesc = request.POST.get('pdesc')
        pjm = request.POST.get('pjm')
        pdm = request.POST.get('pdm')
        QAPL = request.POST.get('QAPL')
        EPL = request.POST.get('EPL')
        plan_start = request.POST.get('pstart')
        plan_end = request.POST.get('pend')
        practical_start = request.POST.get('astart')
        practical_end = request.POST.get('aend')
        count = ProjectInformation.objects.filter(username=username).count()


