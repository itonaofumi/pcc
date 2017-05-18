# -*- coding: utf-8 -*-
from maya import cmds
from maya import mel
from maya import OpenMayaUI as omui 
try:
    from PySide2.QtCore import * 
    from PySide2.QtGui import * 
    from PySide2.QtWidgets import *
    from PySide2 import __version__
    from shiboken2 import wrapInstance 
except ImportError:
    from PySide.QtCore import * 
    from PySide.QtGui import * 
    from PySide import __version__
    from shiboken import wrapInstance
import os.path

mayaMainWindowPtr = omui.MQtUtil.mainWindow() 
mayaMainWindow = wrapInstance(long(mayaMainWindowPtr), QWidget) 

class PccUI(QWidget):
    def __init__(self, *args, **kwargs):
        super(PccUI, self).__init__(*args, **kwargs)
        self.setParent(mayaMainWindow)
        self.setWindowFlags(Qt.Window)
        self.setObjectName('pcc')
        self.setWindowTitle('Physical Controller Connector')
        self.setGeometry(50, 50, 800, 400)
        self.initUI()

    def initUI(self):
        mainLayout = QVBoxLayout()

#------------------------------------------------------------------------------
        portLabel = QLabel("Port:")
        portLine = QLineEdit("3000")
        portLine.setMinimumWidth(40)
        portOpenButton = QPushButton("Open")
        trackLabel = QLabel("Track:")
        trackLcd = QLCDNumber()
        trackLcd.setMaximumHeight(23)
        ccLabel = QLabel("CC:")
        ccLcd = QLCDNumber()
        ccLcd.setMaximumHeight(23)
        
        firstLayout = QHBoxLayout()
        firstLayout.addWidget(portLabel)
        firstLayout.addWidget(portLine)
        firstLayout.addWidget(portOpenButton)
        firstLayout.addStretch()
        firstLayout.addWidget(trackLabel)
        firstLayout.addWidget(trackLcd)
        firstLayout.addWidget(ccLabel)
        firstLayout.addWidget(ccLcd)

        mainLayout.addLayout(firstLayout)

#------------------------------------------------------------------------------
        csvOpenButton = QPushButton("Open")
        csvSaveButton = QPushButton("Save")
        csvLine = QLineEdit()
        portLine.setMaximumWidth(500)

        secondLayout = QHBoxLayout()
        secondLayout.addWidget(csvOpenButton)
        secondLayout.addWidget(csvSaveButton)
        secondLayout.addWidget(csvLine)

        mainLayout.addLayout(secondLayout)

#------------------------------------------------------------------------------
        thirdLayout = QHBoxLayout()
        thirdLayout.addWidget(self._makeTableWidget())

        mainLayout.addLayout(thirdLayout)

#------------------------------------------------------------------------------
        addRowButton = QPushButton("Add Row")
        delRowButton = QPushButton("Delete Row")
        insRowButton = QPushButton("Insert Row")
        delSelButton = QPushButton("Delete Selected Row")

        fourthLayout = QHBoxLayout()
        fourthLayout.addWidget(addRowButton)
        fourthLayout.addWidget(delRowButton)
        fourthLayout.addWidget(insRowButton)
        fourthLayout.addWidget(delSelButton)

        mainLayout.addLayout(fourthLayout)

#------------------------------------------------------------------------------
        self.setLayout(mainLayout)

    def _makeTableWidget(self):
        """
        QTableWidgetを作成する関数
        """
        tableWidget = QTableWidget()
        headerLabels = [ "Track", "CC", "Connect", "Scale", "Offset (0.0-1.0)",
                "Attr Initial", "Attribute"]
        tableWidget.setColumnCount(len(headerLabels))
        tableWidget.setHorizontalHeaderLabels(headerLabels)
        tableWidget.verticalHeader().setVisible(False)

        try:
            tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)

        except:
            tableWidget.horizontalHeader().setResizeMode(QHeaderView.Interactive)

        tableWidget.setAlternatingRowColors(True)
        tableWidget.horizontalHeader().setStretchLastSection(True)
        dataList = [
            ["1", "1", "1", "10", "0.5", "0", "pCube1.tx"],
            ["1", "2", "1", "10", "0.5", "0", "pCube1.ty"],
            ["1", "3", "1", "10", "0.5", "0", "pCube1.tz"]
        ]
        tableWidget.setRowCount(len(dataList))

        for row, colData in enumerate(dataList):

            for col, value in enumerate(colData):
                item = QTableWidgetItem(value)
                tableWidget.setItem(row, col, item)

        return tableWidget


    def button_onClicked(self):
        print 'doOK'

    def doCancel(self):
        self.close()


def main():
    ui = PccUI()
    ui.show()
    return ui


if __name__ == '__main__':
    main()
