# 定义projects app的urls路径

from django.urls import path, re_path
from . import views

app_name = 'projects'
urlpatterns = [
    # 测试
    path('test/', views.TestView.as_view()),
    # 项目列表的url地址
    path('projects/',  views.ProjectsView.as_view(), name='projects'),
    # 新建项目
    path('create_project/', views.CreateProjectView.as_view(), name='create_project'),
    # 展示单个项目
    re_path('project/(?P<project_id>.*)/(?P<pg_show>PG[1-6])/$', views.ProjectView.as_view()),
    path('project/<project_id>/',  views.ProjectView.as_view(), name='project'),
    # 项目故事线
    path('project/<project_id>/stories/', views.StoriesView.as_view(), name='stories'),
    # 修改项目信息
    re_path('project/(?P<project_id>.*)/update/$', views.ProjectUpdateView.as_view()),
    # 查询项目是否存在
    re_path('project/(?P<project_name>.*)/count/$', views.ProjectCheckView.as_view()),
    # 增加修改设备
    path('addproducts/<project_id>/', views.AddProductsView.as_view(), name='addproducts'),
    # 文件上传
    path('project/<project_id>/documents/', views.Documents.as_view(), name='upload_SOW'),
]
