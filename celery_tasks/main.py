from celery import Celery
import os
import django
# 为celery使用django配置文件进行设置


if not os.getenv('DJANGO_SETTINGS_MODULE'):
    os.environ['DJANGO_SETTINGS_MODULE'] = 'QAPMS.settings.dev'

django.setup()
# 创建celery实例
celery_app = Celery('QAPMS')
# 加载celery配置
celery_app.config_from_object('celery_tasks.config')
# 自动注册celery任务
celery_app.autodiscover_tasks(['celery_tasks.email'])