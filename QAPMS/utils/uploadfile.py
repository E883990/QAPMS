import os

from django import http

from QAPMS.utils.md5 import get_file_md5

def upload_file(save_path, file):
    if os.path.exists(save_path):
        return http.HttpResponse('文件重复')
    else:
        with open(save_path, 'wb') as f:
            for content in file.chunks():
                f.write(content)
        md5 = get_file_md5(save_path)
        return md5
