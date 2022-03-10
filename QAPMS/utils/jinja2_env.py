from jinja2 import Environment
from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import reverse
'''确保可以使用模板引擎中的{{ url('')}}{{static('')}}这类语句'''


def jinja2_environment(**options):
    env = Environment(**options)
    # 自定义语法
    env.globals.update({
        'static': staticfiles_storage.url,  # 语法{{static（'静态文件相对路径'）}}就可以使用了
        'url': reverse,  # 表面使用url,实际调用的是reverse, 语法{{url（'路由命名空间'）}}就可以使用了
    })
    return env
