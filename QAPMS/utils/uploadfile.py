from QAPMS.utils.md5 import get_file_md5

def upload_file(save_path, file):
    with open(save_path, 'wb') as f:
        for content in file.chunks():
            f.write(content)
    md5 = get_file_md5(save_path)
    return md5
