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
import csv

mayaMainWindowPtr = omui.MQtUtil.mainWindow()
mayaMainWindow = wrapInstance(long(mayaMainWindowPtr), QWidget)
g_pcc = None

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

        #----------------------------------------------------------------------
        # Port setting
        #----------------------------------------------------------------------
        self.portLabel = QLabel("Port:")
        self.portLine = QLineEdit("3000")
        self.portLine.setMinimumWidth(40)
        self.portOpenButton = QPushButton("Open")
        self.portOpenButton.clicked.connect(self._portOpenButton_onClicked)
        self.portStatusLabel = QLabel("Port is closed")
        self.trackLabel = QLabel("Track:")
        self.trackLcd = QLCDNumber()
        self.trackLcd.setMaximumHeight(23)
        self.ccLabel = QLabel("CC:")
        self.ccLcd = QLCDNumber()
        self.ccLcd.setMaximumHeight(23)

        firstLayout = QHBoxLayout()
        firstLayout.addWidget(self.portLabel)
        firstLayout.addWidget(self.portLine)
        firstLayout.addWidget(self.portOpenButton)
        firstLayout.addWidget(self.portStatusLabel)
        firstLayout.addStretch()
        firstLayout.addWidget(self.trackLabel)
        firstLayout.addWidget(self.trackLcd)
        firstLayout.addWidget(self.ccLabel)
        firstLayout.addWidget(self.ccLcd)

        mainLayout.addLayout(firstLayout)

        #----------------------------------------------------------------------
        # CSV
        #----------------------------------------------------------------------
        self.csvOpenButton = QPushButton("Open")
        self.csvOpenButton.clicked.connect(self._csvOpenButton_onClicked)
        self.csvSaveButton = QPushButton("Save")
        self.csvSaveButton.clicked.connect(self._csvSaveButton_onClicked)
        self.csvLine = QLineEdit()

        secondLayout = QHBoxLayout()
        secondLayout.addWidget(self.csvOpenButton)
        secondLayout.addWidget(self.csvSaveButton)
        secondLayout.addWidget(self.csvLine)

        mainLayout.addLayout(secondLayout)

        #----------------------------------------------------------------------
        # Table
        #----------------------------------------------------------------------
        thirdLayout = QHBoxLayout()
        self.tableWidget = self._makeTableWidget()
        thirdLayout.addWidget(self.tableWidget)

        mainLayout.addLayout(thirdLayout)

        #----------------------------------------------------------------------
        # Table edit buttons
        #----------------------------------------------------------------------
        self.addRowButton = QPushButton("Add Row")
        self.addRowButton.clicked.connect(self._addRowButton_onClicked)
        self.delRowButton = QPushButton("Delete Row")
        self.delRowButton.clicked.connect(self._delRowButton_onClicked)
        self.insRowButton = QPushButton("Insert Row")
        self.insRowButton.clicked.connect(self._insRowButton_onClicked)
        self.delSelButton = QPushButton("Delete Selected Row")
        self.delSelButton.clicked.connect(self._delSelButton_onClicked)

        fourthLayout = QHBoxLayout()
        fourthLayout.addWidget(self.addRowButton)
        fourthLayout.addWidget(self.delRowButton)
        fourthLayout.addWidget(self.insRowButton)
        fourthLayout.addWidget(self.delSelButton)

        mainLayout.addLayout(fourthLayout)

        self.setLayout(mainLayout)

        #----------------------------------------------------------------------
        # load pref file
        #----------------------------------------------------------------------
        self._load_pref()
        self._openCsv()

    def _load_pref(self):
        prefPath = os.path.expanduser('~') + '/pcc.pref'
        csvPath = os.path.expanduser('~') + '/pcc.csv'
        if (cmds.file(prefPath, query=True, exists=True)):
            open_file = open(prefPath, 'r')
            for line in open_file:
                csvPath = line
            open_file.close()
        self.csvLine.setText(csvPath);

    def _save_pref(self):
        open_file = os.path.expanduser('~') + '/pcc.pref'
        if not (cmds.file(open_file, query=True, exists=True)):
            prefFile = open(open_file, 'w', os.O_CREAT)
        else:
            prefFile = open(open_file, 'w')
        prefFile.write(self.csvLine.text())
        prefFile.close()

    def _portOpenButton_onClicked(self):
        portName = 'pcc:' + self.portLine.text()
        isPortOpen = cmds.commandPort(portName, query=True)
        if not isPortOpen:
            melproc = """
            global proc portData(string $arg){
                python(("pcc.exec_pcc(\\"" + $arg + "\\")"));
            }
            """
            mel.eval(melproc)

            cmds.commandPort(name=portName, echoOutput=False, noreturn=False,
                    prefix="portData")
            self.portStatusLabel.setText("Port is open.")

    def _csvOpenButton_onClicked(self):
        csvPath = self.csvLine.text()
        filePath = QFileDialog.getOpenFileName(self, "Select CSV",
                filter="*.csv", options=QFileDialog.DontUseNativeDialog)
        if not filePath[0] == u'':
            self.csvLine.setText(filePath[0])
            self._openCsv()

    def _openCsv(self):
        # delete all rows
        totalRows =  self.tableWidget.rowCount()
        for i in reversed(xrange(totalRows)):
            self.tableWidget.removeRow(i)

        # open and load csv
        open_file = open(self.csvLine.text(), 'r')
        reader = csv.reader(open_file)
        header = next(reader)
        csvList = []
        for r in reader:
            csvList.append(r)

        # write table
        self.tableWidget.setRowCount(len(csvList))
        for row, r in enumerate(csvList):
            for col, c in enumerate(r):
                item = QTableWidgetItem(c)
                self.tableWidget.setItem(row, col, item)
        open_file.close()

        print 'csv loaded.'
        self._save_pref()

    def _csvSaveButton_onClicked(self):
        csvPath = self.csvLine.text()
        if not (cmds.file(csvPath, query=True, exists=True)):
            csvFile = open(csvPath, 'w', os.O_CREAT)
        else:
            csvFile = open(csvPath, 'w')

        writer = csv.writer(csvFile, lineterminator='\n')

        # write first row is header label
        colData = ['Track', 'CC', 'Connect', 'Scale', 'Offset',
                'Attr Initial', 'Attribute']
        writer.writerow(colData)

        rows = self.tableWidget.rowCount()
        cols = self.tableWidget.columnCount()
        for row in xrange(rows):
            colData = []
            for col in xrange(cols):
                colData.append(self.tableWidget.item(row, col).text())
            writer.writerow(colData)
        csvFile.close()

        print 'csv saved.'
        self._save_pref()

    def _addRowButton_onClicked(self):
        self.tableWidget.insertRow(self.tableWidget.rowCount())

    def _delRowButton_onClicked(self):
        self.tableWidget.removeRow(self.tableWidget.rowCount() - 1)

    def _insRowButton_onClicked(self):
        if not self.tableWidget.currentRow() == -1:
            self.tableWidget.insertRow(self.tableWidget.currentRow())

    def _delSelButton_onClicked(self):
        if not self.tableWidget.currentRow() == -1:
            self.tableWidget.removeRow(self.tableWidget.currentRow())

    def _makeTableWidget(self):
        tableWidget = QTableWidget()
        headerLabels = ["Track", "CC", "Connect", "Scale", "Offset (0.0-1.0)",
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
            ["1", "1", "0", "1", "0.5", "0", "pCube1.tx"]
        ]
        tableWidget.setRowCount(len(dataList))

        for row, colData in enumerate(dataList):
            for col, value in enumerate(colData):
                item = QTableWidgetItem(value)
                tableWidget.setItem(row, col, item)

        return tableWidget


def readTable():
    tableData = []
    for r in xrange(g_pcc.tableWidget.rowCount()):
        colData = []
        for c in xrange(g_pcc.tableWidget.columnCount()):
            colData.append(g_pcc.tableWidget.item(r, c).text())
        tableData.append(colData)


'''
_track_num = 1
_cc_num = 1
def exec_pcc(arg):
    #print 'Recieved: ', arg

    # 大量のMIDI情報が送られてくると連結された状態になってしまうので、
    # まず'start', 'end'でsplit
    arg = filter(lambda w: len(w) > 0, re.split('start,|,end', arg))
    #print arg

    # さらに'ch', 'value'を,でsplit
    msg_list = []
    for m in arg:
        m = m.split(',')
        msg_list.append(m)
    #print msg_list
    '''
    ['cc', 'value']
    cc: 0 - 128
    value: 0.0 - 1.0
    '''

    table = read_table() 
    print table
    '''
    colm[0]:track number
    colm[1]:channel number
    colm[2]:connect 0:off 1:on
    colm[3]:scale
    colm[4]:slider offset value
    colm[5]:attribute initial value
    colm[6]:attribute name
    '''

    # fader
    for m in msg_list:
        for colm in table:
            if colm[2] == '1': # connect
                if _track_num == int(colm[0]): # match track
                    if m[0] == colm[1]: # match cc
                        if not colm[6] == '': # attribute name
                            offset = float(m[1]) - float(colm[4])
                            mc.setAttr(colm[6], float(colm[5])
                                    + (offset * float(colm[3])))
                    elif int(m[0]) == int(colm[1]) + 20:
                        # ボタン処理（対象アトリビュートにキーを打つ）
                        if not colm[6] == '': # attribute name
                            mc.setKeyframe(colm[6])

    # track
    MIN_TRACK_NUM = 1
    MAX_TRACK_NUM = 4
    global _track_num

    if msg_list[0][0] == '58' and msg_list[0][1] == '1':
        if _track_num == MIN_TRACK_NUM:
            _track_num = MAX_TRACK_NUM
        else:
            _track_num = _track_num - 1
        mc.textFieldGrp('trackNum', edit=True, text=_track_num)
    elif msg_list[0][0] == '59' and msg_list[0][1] == '1':
        if _track_num == MAX_TRACK_NUM:
            _track_num = MIN_TRACK_NUM
        else:
            _track_num = _track_num + 1
        mc.textFieldGrp('trackNum', edit=True, text=_track_num)

    global _cc_num
    _cc_num = msg_list[0][0]
    mc.textFieldGrp('ccNum', edit=True, text=_cc_num)

    # playback control
    if msg_list[0][0] == '41' and msg_list[0][1] == '1':
        mc.play(forward=True)
    elif msg_list[0][0] == '42' and msg_list[0][1] == '1':
        mc.play(state=False)
    elif msg_list[0][0] == '43' and msg_list[0][1] == '1':
        mm.eval('playButtonStepBackward;')
    elif msg_list[0][0] == '44' and msg_list[0][1] == '1':
        mm.eval('playButtonStepForward;')
'''

def main():
    global g_pcc
    g_pcc = PccUI()
    g_pcc.show()
    return g_pcc


if __name__ == '__main__':
    main()
