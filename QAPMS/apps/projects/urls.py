'''定义projects app的urls路径'''
from django.urls import path
from . import views

app_name = 'projects'
urlpatterns = [
    path('projects/',  views.ProjectsView.as_view(), name='projects'),
    path('project/<int:project_id>/',  views.ProjectView.as_view(), name='project'),
    path('test/',  views.TestView.as_view(), name='test'),
]
