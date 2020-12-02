#!/usr/bin/env python
# coding=utf-8
import sys
from ui import Ui_MainWindow
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import QtGui
from Worker import WorkThread
from PyQt5.QtCore import QTimer, QDateTime
from PyQt5.QtGui import QIcon


class ControlBoard(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(ControlBoard, self).__init__()
        self.setupUi(self)

        self.start.clicked.connect(self.__start)
        self.stop.clicked.connect(self.__stop)
        timer = QTimer(self)
        timer.timeout.connect(self.__showtime)
        timer.start()

        self.__sub_thread = WorkThread('s3-eth1')

        self.__run = False

        self.__first_run = True

    def outputWritten(self, msg):
        if not self.__run:
            return
        text = msg['text']
        if msg['type'] == 'info':
            box = self.info
        else:
            box = self.attack
        cursor = box.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertText(text)
        box.setTextCursor(cursor)
        box.ensureCursorVisible()

    def __showtime(self):
        currentTime = QDateTime.currentDateTime()
        text = currentTime.toString()
        self.datetime.setText(" " + text)

    def __stop(self):
        if self.__run:
            self.outputWritten({'text': 'Q01-SAFE SYSTEM PAUSE...\n', 'type': 'info'})
        self.__run = False

    def __start(self):
        if not self.__run:
            self.__run = True
        if self.__first_run:
            self.__sub_thread.start()
            self.__sub_thread.trigger.connect(self.outputWritten)
            self.__first_run = False
        self.outputWritten({'text': 'Q01-SAFE SYSTEM START...\n', 'type': 'info'})


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = ControlBoard()
    win.setWindowIcon(QIcon('myicon.svg'))
    win.show()
    sys.exit(app.exec_())
