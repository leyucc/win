import os
import urllib.request
from io import BytesIO

from PIL import Image
import cv2
from PyQt5.QtGui import QPixmap


def getQPixmapFromFile(fileUrl) -> QPixmap:
    name = os.path.split(fileUrl)[1]
    ext = os.path.splitext(name)[1].lower()
    q = QPixmap()
    if ext == '.mp4':
        q.loadFromData(getVideoFirstPic(fileUrl))
    else:
        q = QPixmap(fileUrl)
    return q


def getVideoFirstPic(videoUrl) -> bytes:
    vidcap = cv2.VideoCapture(videoUrl)
    success, image = vidcap.read()
    lis = cv2.imencode('.jpg', image)[1]
    vidcap.release()
    bs = bytes(lis)
    return bs
    # cv2.imwrite("frame%d.jpg" % count, image)     # save frame as JPEG file


def zoomPic(url, maxPx=2000, minPx=128):
    if not os.path.exists(url):
        return
    im = Image.open(url)
    x, y = im.size  # 读取图片尺寸（像素）
    if max(x, y) <= maxPx and min(x, y) >= minPx:
        return
    if max(x, y) > maxPx:
        if x > y:
            x_s = maxPx  # 定义缩小后的标准宽度
            y_s = int(y * x_s / x)  # 基于标准宽度计算缩小后的高度
        else:
            y_s = maxPx
            x_s = int(x * y_s / y)
        im = im.resize((x_s, y_s), resample=Image.LANCZOS)  # 改变尺寸，保持图片高品质
        im.save(url)


def enumFiles(folder, urls: list):
    if os.path.exists(folder):
        for item in os.listdir(folder):
            subPath = os.path.join(folder, item)
            if os.path.isdir(subPath):
                enumFiles(subPath, urls)
            else:
                urls.append(subPath)
    return len(urls)


def createFolderByFile(fileUrl):
    if os.path.exists(fileUrl):
        return True
    try:
        arr = os.path.split(fileUrl)
        if os.path.exists(arr[0]):
            return True
        os.makedirs(arr[0])
        return True
    except Exception as e:
        print(f'出错:{e}')
        return False


def downloadFile(url, saveUrl, maxtimes=10):
    for i in range(maxtimes):
        try:
            with urllib.request.urlopen(url) as res, open(saveUrl, 'wb') as f:
                f.write(res.read())
            return True
        except Exception as e:
            print(e)
    return False
