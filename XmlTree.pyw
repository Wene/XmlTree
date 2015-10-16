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
        self.btn_open.clicked.connect(self.open_file)
        self.btn_close = QPushButton("&Close")
        self.btn_close.clicked.connect(self.close)
        lay_buttons.addWidget(self.btn_open)
        lay_buttons.addWidget(self.btn_close)

    # TODO: Method for demo purposes only. Remove in productive version.
    def fill_tree(self):
        self.tree.clear()
        self.tree.setColumnCount(2)
        self.tree.setHeaderLabels(["Hallo", "Welt"])
        item = QTreeWidgetItem(["Eintrag 1", "Spalte 2"])
        self.tree.addTopLevelItem(item)
        subitem = QTreeWidgetItem(["Eintrag 2", "bla"])
        item.addChild(subitem)
        item.setExpanded(True)
        self.tree.resizeColumnToContents(0)

    def open_file(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Open XML File")
        if filename:                            # False if empty string -> no file selected, nothing to do.
            xml_file = QFile(filename)
            xml_file.open(QIODevice.ReadOnly)
            content = xml_file.readAll()
            xml_file.close()
            print(content)


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
