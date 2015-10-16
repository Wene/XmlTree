#!/usr/bin/env python3

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class Form(QWidget):
    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        lay_main = QVBoxLayout(self)
        self.tree = QTreeWidget()
        lay_main.addWidget(self.tree)
        lay_buttons = QHBoxLayout()
        lay_main.addLayout(lay_buttons)
        self.btn_open = QPushButton("&Open")
        self.btn_open.clicked.connect(self.fill_tree)   # dummy action for test
        self.btn_close = QPushButton("&Close")
        self.btn_close.clicked.connect(self.close)
        lay_buttons.addWidget(self.btn_open)
        lay_buttons.addWidget(self.btn_close)

    def fill_tree(self):
        self.tree.setColumnCount(2)
        item = QTreeWidgetItem(["Eintrag 1", "Spalte 2"])
        self.tree.addTopLevelItem(item)
        subitem = QTreeWidgetItem(["Eintrag 2", "bla"])
        item.addChild(subitem)

if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)

    translator = QTranslator()
    lib_path = QLibraryInfo.location(QLibraryInfo.TranslationsPath)
    translator.load("qt_de.qm", lib_path)
    translator.load("qtbase_de.qm", lib_path)
    app.installTranslator(translator)

    window = Form()
    window.show()

    sys.exit(app.exec_())
