import os
import sys

import requests
from PySide2.QtCore import QThread, Signal
from PySide2.QtGui import QIcon
from PySide2.QtWidgets import (QApplication, QFileDialog, QHBoxLayout, QLabel,
                               QLineEdit, QProgressBar, QPushButton,
                               QVBoxLayout, QWidget)

from dowloader import (get_album_dict, get_all_pic, get_one, get_uid,
                       get_username)


#下载所有相册图片
class Thread(QThread):
    pathSignal = Signal(str)
    statusSignal = Signal(str)
    progressSignal = Signal(int)
    finishSignal1 =  Signal()
    def __init__(self,url,path):
        super(Thread,self).__init__()
        self.url = url
        self.path = path


    def run(self):
        os.chdir(self.path)
        #url = self.uid
        self.uid = get_uid(self.url)
        self.username = get_username(self.uid)
        self.album_dict = get_album_dict(self.uid)
        try:
            os.mkdir(self.username)
            os.chdir(self.username)
        except FileExistsError:
            os.chdir(self.username)
        get_all_pic(self)
        self.statusSignal.emit("下载完成")
        self.progressSignal.emit(0)
        self.finishSignal1.emit()


#进下载微博相册图片
class Thread2(QThread):
    pathSignal = Signal(str)
    statusSignal = Signal(str)
    progressSignal = Signal(int)
    finishSignal2 =  Signal()
    def __init__(self,url,path):
        super(Thread2,self).__init__()
        self.url = url
        self.path = path

    def run(self):
        os.chdir(self.path)
        self.uid = get_uid(self.url)
        self.username = get_username(self.uid)
        self.album_dict = get_album_dict(self.uid)
        try:
            os.mkdir(self.username)
            os.chdir(self.username)
        except FileExistsError:
            os.chdir(self.username)
        get_one(self)
        self.statusSignal.emit("下载完成")
        self.progressSignal.emit(0)
        self.finishSignal2.emit()



class Form(QWidget):

    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        # Create widgets
        self.setWindowTitle("微博相册下载")
        self.setWindowIcon(QIcon('assets/icon.png'))
        self.setFixedSize(380,220)
        self.labelPosition = QLabel('路径:')
        self.labelUrl = QLabel('链接:')
        self.editPosition = QLineEdit('.')
        self.editUrl = QLineEdit()
        self.pathLabel = QLabel("下载位置")
        self.statusLabel = QLabel("下载状态")
        self.statusProgress = QProgressBar()
        self.buttonAll = QPushButton("全部相册")
        self.buttonOne = QPushButton("仅微博配图")
        self.buttonExplorer = QPushButton("浏览")
        # Create layout and add widgets
        self.layout = QVBoxLayout()
        self.layout1 = QHBoxLayout()
        self.layout2 = QHBoxLayout()
        self.layout3 = QHBoxLayout()
        self.layout2.addWidget(self.labelPosition)
        self.layout2.addWidget(self.editPosition)
        self.layout2.addWidget(self.buttonExplorer)
        self.layout.addLayout(self.layout2)
        self.layout3.addWidget(self.labelUrl)
        self.layout3.addWidget(self.editUrl)
        self.layout.addLayout(self.layout3)
        self.layout.addWidget(self.pathLabel)
        self.layout.addWidget(self.statusLabel)
        self.layout.addWidget(self.statusProgress)
        self.layout1.addWidget(self.buttonAll)
        self.layout1.addWidget(self.buttonOne)
        self.layout.addLayout(self.layout1)
        self.setLayout(self.layout)

        self.buttonAll.clicked.connect(self.all_album)
        self.buttonOne.clicked.connect(self.single_album)
        self.buttonExplorer.clicked.connect(self.chooseDirectory)
        
    def chooseDirectory(self):
        choosed_path = QFileDialog.getExistingDirectory(self,"选择下载位置")
        self.editPosition.setText(choosed_path)

    def all_album(self):
        self.buttonOne.setDisabled(True)
        self.buttonAll.setDisabled(True)
        self.weibo_thread = Thread(self.editUrl.text(),self.editPosition.text())
        self.weibo_thread.finishSignal1.connect(self.thread_finished)
        self.weibo_thread.pathSignal.connect(self.pathLabel.setText)
        self.weibo_thread.progressSignal.connect(self.statusProgress.setValue)
        self.weibo_thread.statusSignal.connect(self.statusLabel.setText)
        self.weibo_thread.start()

    def single_album(self):
        self.buttonOne.setDisabled(True)
        self.buttonAll.setDisabled(True)
        self.single_thread = Thread2(self.editUrl.text(),self.editPosition.text())
        self.single_thread.finishSignal2.connect(self.thread_finished)
        self.single_thread.pathSignal.connect(self.pathLabel.setText)
        self.single_thread.progressSignal.connect(self.statusProgress.setValue)
        self.single_thread.statusSignal.connect(self.statusLabel.setText)
        self.single_thread.start()

    def thread_finished(self):
        self.buttonOne.setDisabled(False)
        self.buttonAll.setDisabled(False)


if __name__ == '__main__':
    # Create the Qt Application
    app = QApplication(sys.argv)
    # Create and show the form
    form = Form()
    form.show()
    # Run the main Qt loop
    sys.exit(app.exec_())
