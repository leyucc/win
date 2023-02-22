from cls import SingleTask, MultiTask
from myApi import *
import os
import shutil
from PyQt5.QtWidgets import *
import time
from uuid import uuid4
from threading import Thread


class FaceBeautySingle(SingleTask):
    '''人脸美颜单个'''

    def __init__(self, main, editSource, editTemple, editLog, enumButton, startButton, listSource, listTemple, gViewSource, gViewTemple, gViewResult) -> None:
        super().__init__(main, editSource, editTemple, editLog, enumButton, startButton, listSource, listTemple, gViewSource, gViewTemple, gViewResult, '.jpg')
        self.editSource.hide()
        self.main.label_43.hide()

    def work(self, templeUrl, Sharp, Smooth, White):
        try:
            self.log('开始人脸美颜')
            ak, sk = self.main.getAkSk()
            self.setAkSk(ak, sk)
            zoomPic(templeUrl)
            fileName = os.path.split(templeUrl)[1]
            url2 = self.bucket.uploadFile(templeUrl, fileName)
            url = self.aliFace.FaceBeautyRequest(url2, Sharp, Smooth, White)
            self.log('人脸美颜操作成功:' + url)
            return True, url
        except Exception as e:
            self.log(str(e))
            return False, None

    def signgleMergeWork(self, *args):
        templeUrl, Sharp, Smooth, White = args
        ret, url = self.work(templeUrl, Sharp, Smooth, White)
        self.main.gTempFileUrl = ''
        if ret:
            self.main.gTempFileUrl = os.path.join(self.main.gTmpUrl, self.__doc__, str(uuid4()) + self.ext)
            self.log('开始下载')
            ret = downloadFile(url, self.main.gTempFileUrl)
            if ret:
                self.log('下载成功' + self.main.gTempFileUrl)
            else:
                self.log('下载失败')
            q = getQPixmapFromFile(self.main.gTempFileUrl)
            self.gViewResult.setPixmap(q)
            curW = self.gViewResult.width()
            newH = int(self.gViewResult.width() * q.height() / q.width())
            self.gViewResult.resize(curW, newH)

    def btnStartClicked(self):
        items1 = self.listTemple.selectedItems()
        if len(items1) <= 0:
            self.log('请先选中一个模板')
            return
        templeUrl = items1[0].text()
        Sharp = float(self.main.horizontalSlider_5.value() * 0.01)
        Smooth = float(self.main.horizontalSlider_6.value() * 0.01)
        White = float(self.main.horizontalSlider_7.value() * 0.01)

        if self.workThread is None:
            self.workThread = Thread(target=self.signgleMergeWork, args=((templeUrl, Sharp, Smooth, White)))
        elif self.workThread.is_alive():
            self.log('还在融合中,请稍后再操作')
            return
        else:
            self.workThread = Thread(target=self.signgleMergeWork, args=((templeUrl, Sharp, Smooth, White)))
        self.workThread.start()


class FaceBeautyMulti(MultiTask):
    '''人脸美颜批量'''

    def __init__(self, main, editSource, editTemple, editFail, editMove, editResult, editLog, buttons) -> None:
        super().__init__(main, editSource, editTemple, editFail, editMove, editResult, editLog, buttons)

    def taskSingle(self, templeUrl, Sharp, Smooth, White) -> tuple:
        try:
            self.log('开始人脸美颜操作')
            ak, sk = self.main.getAkSk()
            self.setAkSk(ak, sk)
            zoomPic(templeUrl, 1999)
            fileName = os.path.split(templeUrl)[1]
            url2 = self.bucket.uploadFile(templeUrl, fileName)
            url = self.aliFace.FaceBeautyRequest(url2, Sharp, Smooth, White)
            self.log('操作成功!')
            return True, url
        except Exception as e:
            self.log(str(e))
            return False, ''

    def work(self):
        templeUrl = self.editTemple.toPlainText().strip()  # 模板文件夹
        moveUrl = self.editMove.toPlainText().strip()  # 成功后转移文件夹
        failUrl = self.editFail.toPlainText().strip()  # 失败转移文件夹
        saveUrl = self.editResult.toPlainText().strip()  # 保存结果文件夹

        Sharp = float(self.main.horizontalSlider_8.value() * 0.01)
        Smooth = float(self.main.horizontalSlider_9.value() * 0.01)
        White = float(self.main.horizontalSlider_10.value() * 0.01)
        while self.state:
            temples = []
            enumFiles(templeUrl, temples)
            for j, temple in enumerate(temples):
                if self.state == False:
                    break
                templeName = os.path.split(temple)[1]
                name = os.path.split(temple)[0]
                name = os.path.split(name)[1]  # 取回所在文件夹的名字了
                templeMiddle = temple.replace(templeUrl, '')  # 模板文件地址 去掉总文件夹
                self.log(f'正在处理{j+1}/{len(temples)}个模板:{name}')
                result, data = self.taskSingle(temple, Sharp, Smooth, White)
                saveUrl1 = saveUrl + templeMiddle
                moveUrl1 = moveUrl + templeMiddle
                failUrl1 = failUrl + templeMiddle
                if result:
                    createFolderByFile(saveUrl1)
                    ret = downloadFile(data, saveUrl1)
                    if ret:
                        self.log(f'{templeName}_{name}合成结果已经保存')
                        createFolderByFile(moveUrl1)
                        shutil.move(temple, moveUrl1)
                        self.log(f'合成成功,转移已成功模板{temple}')
                    else:
                        self.log('下载失败超过重试次数')
                if not result or not ret:
                    createFolderByFile(failUrl1)
                    shutil.move(temple, failUrl1)
                    if not result:
                        msg = '融合失败,转移至失败目录'
                    else:
                        msg = '下载失败,转移至失败目录'
                    self.log(f'{temple}{msg}')
            time.sleep(2)
        self.log('任务已经停止')
