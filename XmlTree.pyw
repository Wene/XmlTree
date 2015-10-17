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

        # restore settings
        self.settings = QSettings("Wene", "XmlTree")
        self.move(self.settings.value("Position", QPoint(50, 50)))
        self.resize(self.settings.value("Size", QSize(300, 300)))

    def closeEvent(self, QCloseEvent):
        # save settings on closing
        self.settings.setValue("Position", self.pos())
        self.settings.setValue("Size", self.size())

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
            self.tree.clear()
            self.tree.setColumnCount(3)
            self.tree.setHeaderLabels(["Name", "Attributes", "Value"])

            xml_file = QFile(filename)
            xml_file.open(QIODevice.ReadOnly)
            xml_reader = QXmlStreamReader(xml_file)

            while not xml_reader.atEnd():
                xml_reader.readNext()
                if xml_reader.isStartElement():
                    item = self.read_xml_to_item(xml_reader)
                    self.tree.addTopLevelItem(item)
                    item.setExpanded(True)          # TODO: call recursively

            xml_reader.clear()
            xml_file.close()
            for i in range(3):
                self.tree.resizeColumnToContents(i)

    def read_xml_to_item(self, xml_reader):
        assert isinstance(xml_reader, QXmlStreamReader)
        item = QTreeWidgetItem()

        name = xml_reader.name()
        attributes = xml_reader.attributes()
        assert isinstance(attributes, QXmlStreamAttributes)
        # TODO: convert attributes into attribute_text
        attribute_text = ""

        text = ""
        # loop til end of this element
        while not xml_reader.isEndElement():
            xml_reader.readNext()
            if xml_reader.isCharacters():
                text = xml_reader.text()
            elif xml_reader.isStartElement():   # recursively scan start elements
                sub_item = self.read_xml_to_item(xml_reader)
                item.addChild(sub_item)
                xml_reader.readNext()           # necessary to avoid isEndElement detection of the sub element

        item.setText(0, name)
        item.setText(1, attribute_text)
        item.setText(2, text)
        return item


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
