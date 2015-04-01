#coding=utf-8

import os, time
from django.http import HttpResponse
from PIL import Image

# def readFile(fn, buf_size=262144):
#     f = open(fn, "rb")
#     while True:
#         c = f.read(buf_size)
#         if c:
#             yield c
#         else:
#             break
#     f.close()


# 文件上传
def handle_uploaded_file(f):
    file_name = ""

    try:
        path = "media/image" + time.strftime('/%Y/%m/%d/%H/%M/%S/')
        if not os.path.exists(path):
            os.makedirs(path)
            file_name = path + f.name
            destination = open(file_name, 'wb+')
            for chunk in f.chunks():
                destination.write(chunk)
            destination.close()
    except Exception, e:
        print e

    return file_name


def show_file(file_name):
    def readFile(file_name, buf_size=262144):
        f = open(file_name, "rb")
        while True:
            c = f.read(buf_size)
            if c:
                yield c
            else:
                break
        f.close()

    response = HttpResponse(readFile(file_name), content_type='application/x-msdownload')

    return response


def make_thumb3(path, thumb_path, size):
    img = Image.open(path)
    width, height = img.size
    if width > height:
        thumb = img.resize((size, int(100 * height / width)), Image.ANTIALIAS)
    else:
        thumb = img.resize((int(100 * width / height), size), Image.ANTIALIAS)

    base, ext = os.path.splitext(os.path.basename(path))
    filename = os.path.join(thumb_path, '%s_thumb.jpg' % (base,))
    # 保存
    thumb.save(filename, quality=70)
    return '%s_thumb.jpg' % base


def make_thumb2(path, thumb_path, size):
    im = Image.open(path)
    im.thumbnail((size, size))
    base, ext = os.path.splitext(os.path.basename(path))
    filename = os.path.join(thumb_path, '%s_thumb.jpg' % (base,))
    im.save(filename, quality=70)
    return '%s_thumb.jpg' % base


def make_thumb(path, thumb_path, size):
    """生成缩略图"""
    img = Image.open(path)
    width, height = img.size
    # 裁剪图片成正方形
    if width > height:
        delta = (width - height) / 2
        box = (delta, 0, width - delta, height)
        region = img.crop(box)
    elif height > width:
        delta = (height - width) / 2
        box = (0, delta, width, height - delta)
        region = img.crop(box)
    else:
        region = img

    # 缩放
    thumb = region.resize((size, size), Image.ANTIALIAS)

    # base, ext = os.path.splitext(os.path.basename(path))
    # filename = '%s_thumb%s' % (base, ext)
    filename = os.path.join(thumb_path, os.path.basename(path))
    # 保存
    if not os.path.exists(thumb_path):
        os.makedirs(thumb_path)
    thumb.save(filename, quality=70)
    return os.path.basename(filename)





def send_sms(mobile, message):
    pass


def send_email(email, message):
    pass