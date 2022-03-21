import os

from django.http import StreamingHttpResponse


def streamDownload(resquest):
    def file_iterator(filepath, chunk_size = 512):
        with open(filepath, 'rb') as f:
            while True:
                con = f.read(512)
                if con:
                    yield con
                else:
                    break
            filename = os.path.abspath(__file__) + 'test.txt'
            response = StreamingHttpResponse(file_iterator(filename))
        return response
# 最后程序会将结果打印在显示器上
