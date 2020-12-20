#!/usr/bin/env python

import sys
from PyQt5.QtWidgets import QWidget, QMessageBox, QApplication
from gestionBD import BD

class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 250, 150)
        button=QPushButton('Click me',self)
        self.setWindowTitle('Message box')
        self.show()

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message',
                                     "Are you sure to quit?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

def main():
    nomBD="recettes.bd"
    BD(self,self.nomBD)
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

