import sys
from types import TracebackType
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from Ui_main import Ui_Dialog
import os
import configparser
import shutil
import cls
from check import Check
from FaceFilter import *
from FaceMakeUp import *
from FaceBeauty import *


class MyDialog(QDialog, Ui_Dialog):
    _gameSignal = pyqtSignal(str)  # 不可定义在__init__   必须定义为类成员

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.load()
        self.gTmpUrl = r'.\tmp'
        self.gTempFileUrl = ''
        try:
            if not os.path.exists(self.gTmpUrl):
                os.makedirs(self.gTmpUrl)
        except Exception as e:
            pass
        self.setFixedSize(self.width(), self.height())
        winflags = Qt.WindowType.Dialog
        winflags |= Qt.WindowType.WindowMinimizeButtonHint
        winflags |= Qt.WindowType.WindowCloseButtonHint
        self.setWindowFlags(winflags)
        self.setAcceptDrops(True)
        self.gViewResult.mouseDoubleClickEvent = self.ongViewResultDbclick

        self.FaceMergeSingle = cls.FaceMergeSingle(self, self.editSourcea, self.editTemplea, self.editLoga, self.enumButton,
                                                   self.startButtona, self.listSource, self.listTemple,
                                                   self.gViewSource, self.gViewTemple, self.gViewResult)

        self.FaceMergeMulti = cls.FaceMergeMulti(self, self.editSource, self.editTemple, self.editFail, self.editMove,
                                                 self.editResult, self.editLog,
                                                 [self.pushButtona, self.pushButtonb, self.pushButtonc,
                                                  self.pushButtond, self.pushButtone, self.startButton, self.stopButton],
                                                 )

        self.MergeVideoSingle = cls.MergeVideoSingle(self, self.editSourcea_2, self.editTemplea_2, self.editLoga_2, self.enumButton_2,
                                                     self.startButtona_2, self.listSource_2, self.listTemple_2,
                                                     self.gViewSource, self.gViewTemple, self.gViewResult)

        self.MergeVideoMulti = cls.MergeVideoMulti(self, self.editSource_2, self.editTemple_2, self.editFail_2, self.editMove_2,
                                                   self.editResult_2, self.editLog_2,
                                                   [self.pushButtona_2, self.pushButtonb_2, self.pushButtonc_2,
                                                    self.pushButtond_2, self.pushButtone_2, self.startButton_2, self.stopButton_2]
                                                   )

        self.SegmentHDSingle = cls.SegmentHDSingle(self, self.editSourcea_7, self.editTemplea_7, self.editLoga_7, self.enumButton_7,
                                                   self.startButtona_7, self.listSource_7, self.listTemple_7,
                                                   self.gViewSource, self.gViewTemple, self.gViewResult)

        self.SegmentHDMulti = cls.SegmentHDMulti(self, self.editSource_7, self.editTemple_7, self.editFail_7, self.editMove_7,
                                                 self.editResult_7, self.editLog_7,
                                                 [self.pushButtona_7, self.pushButtonb_7, self.pushButtonc_7,
                                                  self.pushButtond_7, self.pushButtone_7, self.startButton_7, self.stopButton_7]
                                                 )

        self.SegmentBodySingle = cls.SegmentBodySingle(self, self.editSourcea_5, self.editTemplea_5, self.editLoga_5, self.enumButton_5,
                                                       self.startButtona_5, self.listSource_5, self.listTemple_5,
                                                       self.gViewSource, self.gViewTemple, self.gViewResult)

        self.SegmentBodyMulti = cls.SegmentBodyMulti(self, self.editSource_5, self.editTemple_5, self.editFail_5, self.editMove_5,
                                                     self.editResult_5, self.editLog_5,
                                                     [self.pushButtona_5, self.pushButtonb_5, self.pushButtonc_5,
                                                      self.pushButtond_5, self.pushButtone_5, self.startButton_5, self.stopButton_5]
                                                     )

        self.FaceFilterSingle = FaceFilterSingle(self, self.editSourcea_3, self.editTemplea_3, self.editLoga_3, self.enumButton_3,
                                                 self.startButtona_3, self.listSource_3, self.listTemple_3,
                                                 self.gViewSource, self.gViewTemple, self.gViewResult)

        self.FaceFilterMulti = FaceFilterMulti(self, self.editSource_3, self.editTemple_3, self.editFail_3, self.editMove_3,
                                               self.editResult_3, self.editLog_3,
                                               [self.pushButtona_3, self.pushButtonb_3, self.pushButtonc_3,
                                                self.pushButtond_3, self.pushButtone_3, self.startButton_3, self.stopButton_3]
                                               )

        self.FaceMakeupSingle = FaceMakeupSingle(self, self.editSourcea_4, self.editTemplea_4, self.editLoga_4, self.enumButton_4,
                                                 self.startButtona_4, self.listSource_4, self.listTemple_4,
                                                 self.gViewSource, self.gViewTemple, self.gViewResult)

        self.FaceMakeupMulti = FaceMakeupMulti(self, self.editSource_4, self.editTemple_4, self.editFail_4, self.editMove_4,
                                               self.editResult_4, self.editLog_4,
                                               [self.pushButtona_4, self.pushButtonb_4, self.pushButtonc_4,
                                                self.pushButtond_4, self.pushButtone_4, self.startButton_4, self.stopButton_4]
                                               )

        self.FaceBeautySingle = FaceBeautySingle(self, self.editSourcea_6, self.editTemplea_6, self.editLoga_6, self.enumButton_6,
                                                 self.startButtona_6, self.listSource_6, self.listTemple_6,
                                                 self.gViewSource, self.gViewTemple, self.gViewResult)

        self.FaceBeautyMulti = FaceBeautyMulti(self, self.editSource_6, self.editTemple_6, self.editFail_6, self.editMove_6,
                                               self.editResult_6, self.editLog_6,
                                               [self.pushButtona_6, self.pushButtonb_6, self.pushButtonc_6,
                                                self.pushButtond_6, self.pushButtone_6, self.startButton_6, self.stopButton_6]
                                               )

        self.editArr = [self.editAppKeyId, self.editSecretKey]
        for item in self.editArr:
            item.textChanged.connect(self.textChanged)
        self.horizontalSlider.valueChanged.connect(self.horizontalSliderChange)
        self.horizontalSlider_2.valueChanged.connect(self.horizontalSliderChange)
        self.horizontalSlider_3.valueChanged.connect(self.horizontalSliderChange)
        self.horizontalSlider_4.valueChanged.connect(self.horizontalSliderChange)
        self.horizontalSlider_5.valueChanged.connect(self.horizontalSliderChange)
        self.horizontalSlider_6.valueChanged.connect(self.horizontalSliderChange)
        self.horizontalSlider_7.valueChanged.connect(self.horizontalSliderChange)
        self.horizontalSlider_8.valueChanged.connect(self.horizontalSliderChange)
        self.horizontalSlider_9.valueChanged.connect(self.horizontalSliderChange)
        self.horizontalSlider_10.valueChanged.connect(self.horizontalSliderChange)

    def horizontalSliderChange(self):
        obj: QSlider = self.sender()
        name = obj.objectName()
        value = float(obj.value() * 0.01)
        value = round(value, 2)
        if name == 'horizontalSlider':
            self.label_52.setText(str(value))
        elif name == 'horizontalSlider_2':
            self.label_53.setText(str(value))
        elif name == 'horizontalSlider_3':
            self.label_54.setText(str(value))
        elif name == 'horizontalSlider_4':
            self.label_59.setText(str(value))
        elif name == 'horizontalSlider_5':
            self.label_66.setText(str(value))
        elif name == 'horizontalSlider_6':
            self.label_62.setText(str(value))
        elif name == 'horizontalSlider_7':
            self.label_65.setText(str(value))
        elif name == 'horizontalSlider_8':
            self.label_67.setText(str(value))
        elif name == 'horizontalSlider_9':
            self.label_69.setText(str(value))
        elif name == 'horizontalSlider_10':
            self.label_71.setText(str(value))

    def logger(self, func):
        def inner(self, *args, **kwargs):  # 1
            try:
                func(self, *args, **kwargs)  # 2
            except BaseException:
                print('error')
        return inner

    def getAkSk(self):
        ak = self.editAppKeyId.text().strip()
        sk = self.editSecretKey.text().strip()
        return ak, sk

    def ongViewResultDbclick(self, a0: QMouseEvent):
        index = self.tabWidget_2.currentIndex()
        if index == 0:
            clsObj = self.FaceMergeSingle
        elif index == 1:
            clsObj = self.MergeVideoSingle
        elif index == 2:
            clsObj = self.FaceFilterSingle
        elif index == 3:
            clsObj = self.FaceMakeupSingle
        elif index == 4:
            clsObj = self.FaceBeautySingle
        elif index == 5:
            clsObj = self.SegmentBodySingle
        elif index == 6:
            clsObj = self.SegmentHDSingle
        log = clsObj.log
        ext = clsObj.ext
        if os.path.exists(self.gTempFileUrl):
            import subprocess
            subprocess.call(f'explorer.exe /select,"{self.gTempFileUrl}"')
            return
        else:
            log('还没生成文件,呢请先生成后再来保存!')
            return

        ret = QFileDialog.getSaveFileName(self, '请选择文件', '', '*' + ext)
        if ret[0] != '' and os.path.exists(self.gTempFileUrl):
            try:
                self.gViewResult.pixmap().save(ret[0], 'jpg', 100)
                shutil.copy(self.gTempFileUrl, ret[0])
                log('保存生成结果:' + ret[0])
            except Exception as e:
                log('保存图片到文件失败!' + str(e))
        else:
            if os.path.exists(self.gTempFileUrl) == False:
                log('还没生成文件,呢请先生成后再来保存!')

    def load(self):
        config = configparser.ConfigParser()  # 类实例化
        config.read('./config.ini')
        section = config.sections()
        if 'main' not in section:
            return
        for item in self.findChildren(QTextEdit):
            item: QTextEdit
            key = item.objectName()
            if key.startswith('editLog'):
                continue
            if key in config['main']:
                item.setText(config['main'][key])
        for item in self.findChildren(QLineEdit):
            item: QLineEdit
            key = item.objectName()
            if key in config['main']:
                item.setText(config['main'][key])

        for item1 in self.findChildren(QSlider):
            item1: QSlider
            key = item1.objectName()
            if key in config['main']:
                try:
                    value = int(config['main'][key])
                    item1.setValue(value)
                    name = item1.objectName()
                    value = round(value * 0.01, 2)
                    if name == 'horizontalSlider':
                        self.label_52.setText(str(value))
                    elif name == 'horizontalSlider_2':
                        self.label_53.setText(str(value))
                    elif name == 'horizontalSlider_3':
                        self.label_54.setText(str(value))
                    elif name == 'horizontalSlider_4':
                        self.label_59.setText(str(value))
                    elif name == 'horizontalSlider_5':
                        self.label_66.setText(str(value))
                    elif name == 'horizontalSlider_6':
                        self.label_62.setText(str(value))
                    elif name == 'horizontalSlider_7':
                        self.label_65.setText(str(value))
                    elif name == 'horizontalSlider_8':
                        self.label_67.setText(str(value))
                    elif name == 'horizontalSlider_9':
                        self.label_69.setText(str(value))
                    elif name == 'horizontalSlider_10':
                        self.label_71.setText(str(value))

                except Exception as e:
                    continue

        for item in self.findChildren(QListWidget):
            item: QListWidget
            if item.viewMode() == QListView.ViewMode.ListMode:
                key = item.objectName()
                if key in config['main']:
                    try:
                        row = int(config['main'][key])
                        item.setCurrentRow(row)
                    except Exception as e:
                        pass

    def save(self):
        config = configparser.ConfigParser()  # 类实例化
        config.add_section('main')  # 首先添加一个新的section
        arr = self.findChildren(QTextEdit)
        for item in arr:
            try:
                item: QTextEdit
                name = item.objectName()
                if name.startswith('editLog'):
                    continue
                text = item.toPlainText()
                config.set('main', name, text)
            except Exception as e:
                continue
        arr = self.findChildren(QLineEdit)
        for item in arr:
            try:
                item: QLineEdit
                name = item.objectName()
                text = item.text()
                config.set('main', name, text)
            except Exception as e:
                continue
        for item in self.findChildren(QSlider):
            try:
                item: QSlider
                name = item.objectName()
                text = str(item.value())
                config.set('main', name, text)
            except Exception as e:
                continue
        for item in self.findChildren(QListWidget):
            try:
                item: QListWidget
                name = item.objectName()
                if item.viewMode() == QListView.ViewMode.ListMode:
                    text = str(item.currentIndex().row())
                    config.set('main', name, text)
            except Exception as e:
                continue
        config.write(open('./config.ini', 'w'))  # 保存数据

    def textChanged(self):
        obj: QLineEdit = self.sender()
        txt = obj.text()
        if 0 <= txt.find('file:///'):
            obj.setText(txt.replace('file:///', '').replace("/", "\\"))
        self.save()

    def closeEvent(self, a0) -> None:
        import win32api
        win32api.TerminateProcess(-1, 0)
        exit(0)


def myExcepthook(ttype, tvalue, ttraceback: TracebackType):
    print(f"type:{ttype}")
    print(f"value:{tvalue}")
    i = 1
    arr = []
    while ttraceback:
        tracebackCode = ttraceback.tb_frame.f_code
        arr.append(f"module_name:{tracebackCode.co_filename}")
        arr.append(f"co_name:{tracebackCode.co_name}")
        ttraceback = ttraceback.tb_next
        i += 1
    msg = '\n'.join(arr)
    clipboard = QApplication.clipboard()
    clipboard.setText(msg)
    QMessageBox.information(None, '', msg)


if __name__ == '__main__':

    check = Check()
    if check.checkTime():
        sys.excepthook = myExcepthook
        app = QApplication(sys.argv)
        mainWindow = MyDialog()
        # qss = os.path.abspath(__file__)  # 直接用  __file__ pyinstaller打包之后为空字符串
        # qss = os.path.dirname(qss)
        # qss = os.path.join(qss, 'q.qss')
        # f = open(qss, 'r')
        # mainWindow.setStyleSheet(f.read())
        # f.close()
        iconUrl = os.path.abspath(__file__)  # 直接用  __file__ pyinstaller打包之后为空字符串
        iconUrl = os.path.dirname(iconUrl)
        iconUrl = os.path.join(iconUrl, 'logo.ico')
        icon = QIcon()
        icon.addPixmap(QPixmap(iconUrl), QIcon.Normal, QIcon.Off)
        mainWindow.setWindowIcon(icon)

        mainWindow.show()
        sys.exit(app.exec_())
