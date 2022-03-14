'''定义projects app的urls路径'''
from django.urls import path
from . import views

app_name = 'projects'
urlpatterns = [
    # 项目列表的url地址
    path('projects/',  views.ProjectsView.as_view(), name='projects'),
    # 单个项目的url地址
    path('project/<int:project_id>/',  views.ProjectView.as_view(), name='project'),
    # 新建项目
    path('create_project/', views.CreateProjectView.as_view(),name='create_project'),
    # 增加项目成员

]
