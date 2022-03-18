# 定义projects app的urls路径

from django.urls import path, re_path
from . import views

app_name = 'projects'
urlpatterns = [
    # 项目故事线
    path('project/<int:project_id>/stories/', views.StoriesView.as_view(), name='stories'),
    # 增加设备
    path('addproducts/<int:project_id>', views.AddProductsView.as_view(), name='addproducts'),
    # 测试
    path('test/', views.TestView.as_view()),
    # 项目列表的url地址
    path('projects/',  views.ProjectsView.as_view(), name='projects'),
    # 单个项目的url地址
    path('project/<int:project_id>/',  views.ProjectView.as_view(), name='project'),
    # 新建项目
    path('create_project/', views.CreateProjectView.as_view(), name='create_project'),
    # 查询项目是否存在
    re_path('project/(?P<project_name>.*)/count', views.ProjectCheckView.as_view()),
]
