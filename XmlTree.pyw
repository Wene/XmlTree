#!/usr/bin/env python3

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class Form(QWidget):
    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        self.setWindowTitle("XmlTree v0.1")

        lay_main = QVBoxLayout(self)
        self.tree = QTreeWidget()
        self.tree.setHeaderHidden(True)
        lay_main.addWidget(self.tree)
        lay_buttons = QHBoxLayout()
        lay_main.addLayout(lay_buttons)
        self.btn_open = QPushButton("Ö&ffnen")
        self.btn_open.clicked.connect(self.open_file)
        self.btn_close = QPushButton("&Schliessen")
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

    def open_file(self):
        last_filename = self.settings.value("Filename", ".")
        filename, _ = QFileDialog.getOpenFileName(self, "XML Datei öffnen", last_filename,
                                                  "XML Dateien (*.xml);;Alle Dateien (*)")
        if filename:                            # False if empty string -> no file selected, nothing to do.
            self.tree.clear()
            self.tree.setColumnCount(3)
            self.tree.setHeaderHidden(False)
            self.tree.setHeaderLabels(["Name", "Attribute", "Inhalt"])

            xml_file = QFile(filename)
            xml_file.open(QIODevice.ReadOnly)
            self.settings.setValue("Filename", filename)    # save filename in settings for next use
            xml_reader = QXmlStreamReader(xml_file)

            while not xml_reader.atEnd():
                xml_reader.readNext()
                if xml_reader.isStartElement():
                    item = self.read_xml_to_item(xml_reader)
                    self.tree.addTopLevelItem(item)
                    self.expand_recursively(item)
            # TODO: error handling

            xml_reader.clear()
            xml_file.close()
            for i in range(3):
                self.tree.resizeColumnToContents(i)

    def expand_recursively(self, item):
        assert isinstance(item, QTreeWidgetItem)
        item.setExpanded(True)
        for i in range(item.childCount()):
            self.expand_recursively(item.child(i))

    # read the XML structure and return QTreeWidgetItem
    def read_xml_to_item(self, xml_reader):
        assert isinstance(xml_reader, QXmlStreamReader)
        item = QTreeWidgetItem()

        # get name and attributes from current element
        name = xml_reader.name()
        attributes = xml_reader.attributes()
        attribute_text = ""
        assert isinstance(attributes, QXmlStreamAttributes)

        # convert attributes into text
        count = attributes.count()
        for i in range(count):
            attr = attributes.at(i)
            assert isinstance(attr, QXmlStreamAttribute)
            attribute_text += attr.name() + "=" + attr.value()
            if i < count - 1:
                attribute_text += "; "

        # read next element - may be a text, end or start element.
        xml_reader.readNext()
        text = ""
        while not xml_reader.isEndElement():    # loop til end of this element
            if xml_reader.isCharacters():       # if it is text, it belongs to this element
                text = xml_reader.text()
            elif xml_reader.isStartElement():   # a start element at this point must be a sub element.
                sub_item = self.read_xml_to_item(xml_reader)    # scan elements recursively
                item.addChild(sub_item)
            xml_reader.readNext()

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
