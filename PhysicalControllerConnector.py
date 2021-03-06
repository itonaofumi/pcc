# -*- coding: utf-8 -*-
from maya import cmds
from maya import mel
from maya import OpenMayaUI as omui

import os.path
import csv
import re
import json

import pdb

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

        self.pcc_pref = {'port':3000, 'csv_list':[]}
        self.tab_list = list()
        self.current_table = None
        self.current_table_array = None

        self.initUI()

    def initUI(self):
        mainLayout = QVBoxLayout()

        #----------------------------------------------------------------------
        # Port setting
        #----------------------------------------------------------------------
        self.port_lavel = QLabel("Port:")
        self.port_line = QLineEdit("3000")
        self.port_line.setMinimumWidth(40)
        self.port_line.setMaximumWidth(40)
        self.port_line.textChanged.connect(self._port_changed)
        self.port_open_button = QPushButton("Open")
        self.port_open_button.clicked.connect(self._portOpenButton_onClicked)
        self.port_status_label = QLabel("Port is closed")
        self.cc_label = QLabel("CC:")
        self.cc_lcd = QLCDNumber()
        self.cc_lcd.setSegmentStyle(QLCDNumber.Flat)
        self.cc_lcd.display(1)

        self.port_layout = QHBoxLayout()
        self.port_layout.addWidget(self.port_lavel)
        self.port_layout.addWidget(self.port_line)
        self.port_layout.addWidget(self.port_open_button)
        self.port_layout.addWidget(self.port_status_label)
        self.port_layout.addStretch()
        self.port_layout.addWidget(self.cc_label)
        self.port_layout.addWidget(self.cc_lcd)

        mainLayout.addLayout(self.port_layout)

        #----------------------------------------------------------------------
        # CSV
        #----------------------------------------------------------------------
        self.csv_open_button = QPushButton("Open")
        self.csv_save_button = QPushButton("Save")
        self.csv_open_button.clicked.connect(self._csvOpenButton_onClicked)
        self.csv_save_button.clicked.connect(self._csvSaveButton_onClicked)
        self.csv_lavel = QLabel("CSV:")
        self.csv_line = QLineEdit()

        self.csv_layout = QHBoxLayout()
        self.csv_layout.addWidget(self.csv_open_button)
        self.csv_layout.addWidget(self.csv_save_button)
        self.csv_layout.addWidget(self.csv_lavel)
        self.csv_layout.addWidget(self.csv_line)

        mainLayout.addLayout(self.csv_layout)

        #----------------------------------------------------------------------
        # Tab
        #----------------------------------------------------------------------

        # Button
        self.add_tab_button = QPushButton("Add Tab")
        self.del_tab_button = QPushButton("Close Tab")
        self.add_tab_button.clicked.connect(self._add_tab)
        self.del_tab_button.clicked.connect(self._del_tab)

        self.tab_button_layout = QHBoxLayout()
        self.tab_button_layout.addWidget(self.add_tab_button)
        self.tab_button_layout.addWidget(self.del_tab_button)
        self.tab_button_layout.addStretch()

        mainLayout.addLayout(self.tab_button_layout)

        # Tab
        self.tab_widget = QTabWidget()
        self.tab_widget.currentChanged.connect(self._update_current_table_array)

        self.tab_layout = QVBoxLayout()
        self.tab_layout.addWidget(self.tab_widget)

        mainLayout.addLayout(self.tab_layout)

        #----------------------------------------------------------------------
        # Edit table buttons
        #----------------------------------------------------------------------
        self.add_row_button = QPushButton("Add Row")
        self.del_row_button = QPushButton("Delete Row")
        self.ins_row_button = QPushButton("Insert Row")
        self.del_sel_button = QPushButton("Delete Selected Row")
        self.add_row_button.clicked.connect(self._addRowButton_onClicked)
        self.del_row_button.clicked.connect(self._delRowButton_onClicked)
        self.ins_row_button.clicked.connect(self._insRowButton_onClicked)
        self.del_sel_button.clicked.connect(self._delSelButton_onClicked)

        self.fourth_layout = QHBoxLayout()
        self.fourth_layout.addWidget(self.add_row_button)
        self.fourth_layout.addWidget(self.del_row_button)
        self.fourth_layout.addWidget(self.ins_row_button)
        self.fourth_layout.addWidget(self.del_sel_button)

        mainLayout.addLayout(self.fourth_layout)

        self.setLayout(mainLayout)

    #--------------------------------------------------------------------------
    # pref
    #--------------------------------------------------------------------------
    def _load_pref_json(self):
        path = os.path.expanduser('~') + '/pcc_pref.json'

        if (cmds.file(path, query=True, exists=True)):
            f = open(path, 'r')
            self.pcc_pref = json.load(f)
            f.close()

            self.port_line.setText(str(self.pcc_pref['port']))

            for path in self.pcc_pref['csv_list']:

                if (path != '' and os.path.isfile(path)):
                    self._add_tab_launch()
                    self.csv_line.setText(path)
                    self._open_csv()

    def _save_pref_json(self):
        path = os.path.expanduser('~') + '/pcc_pref.json'

        if not (cmds.file(path, query=True, exists=True)):
            f = open(path, 'w', os.O_CREAT)
        else:
            f = open(path, 'w')

        json.dump(self.pcc_pref, f)
        f.close()

    #--------------------------------------------------------------------------
    # port
    #--------------------------------------------------------------------------
    def _check_port(self):
        port_name = 'pcc:' + self.port_line.text()
        is_port_open = cmds.commandPort(port_name, query=True)

        if is_port_open:
            self.port_status_label.setText("Port is open.")

    def _port_changed(self):
        self.pcc_pref['port'] = self.port_line.text()
        self._save_pref_json()

    def _portOpenButton_onClicked(self):
        port_name = 'pcc:' + self.port_line.text()
        is_port_open = cmds.commandPort(port_name, query=True)

        if not is_port_open:
            melproc = """
            global proc portData(string $arg){
                python(("pcc.exec_pcc(\\"" + $arg + "\\")"));
            }
            """
            mel.eval(melproc)

            cmds.commandPort(name=port_name, echoOutput=False, noreturn=False,
                    prefix="portData")
            self.port_status_label.setText("Port is open.")

    #--------------------------------------------------------------------------
    # csv
    #--------------------------------------------------------------------------
    def _csvOpenButton_onClicked(self):
        file_path = QFileDialog.getOpenFileName(self, "Select CSV",
                filter="*.csv", options=QFileDialog.DontUseNativeDialog)

        if not file_path[0] == u'':
            self.csv_line.setText(file_path[0])
            self._open_csv()

    def _open_csv(self):

        # update pref's csv_list 
        index = self.tab_widget.currentIndex()
        self.pcc_pref['csv_list'][index] = self.csv_line.text()

        # update current tab name
        file_name = self._get_file_name()
        self.tab_widget.setTabText(index, file_name);

        # delete all rows
        total_rows =  self.current_table.rowCount()

        for i in reversed(xrange(total_rows)):
            self.current_table.removeRow(i)

        # open and load csv
        f = open(self.csv_line.text(), 'r')
        reader = csv.reader(f)
        header = next(reader)
        csvList = []

        for r in reader:
            csvList.append(r)

        # write table
        self.current_table.setRowCount(len(csvList))

        for row, r in enumerate(csvList):
            for col, c in enumerate(r):
                item = QTableWidgetItem(c)
                self.current_table.setItem(row, col, item)

        f.close()

        print 'csv loaded.'
        self._save_pref_json()

    def _csvSaveButton_onClicked(self):
        csv_path = self.csv_line.text()

        if not (cmds.file(csv_path, query=True, exists=True)):
            csvFile = open(csv_path, 'w', os.O_CREAT)
        else:
            csvFile = open(csv_path, 'w')
        writer = csv.writer(csvFile, lineterminator='\n')

        # write first row is header label
        col_data = [
                'CC',
                'Connect',
                'Scale',
                'Offset',
                'Attr Initial',
                'Attribute'
                ]
        writer.writerow(col_data)

        rows = self.current_table.rowCount()
        cols = self.current_table.columnCount()

        for row in xrange(rows):
            col_data = []

            for col in xrange(cols):
                data = self.current_table.item(row, col)

                if (data is not None):
                    col_data.append(data.text())

            writer.writerow(col_data)

        csvFile.close()

        # update pref's csv_list 
        index = self.tab_widget.currentIndex()
        self.pcc_pref['csv_list'][index] = self.csv_line.text()

        # update current tab name
        file_name = self._get_file_name()
        self.tab_widget.setTabText(index, file_name);

        print 'csv saved.'
        self._save_pref_json()

    #--------------------------------------------------------------------------
    # tab
    #--------------------------------------------------------------------------
    def _add_tab(self):
        table = self._make_table_widget()
        table.cellChanged.connect(self._update_current_table_array)
        self.tab_list.append(table)
        self.pcc_pref['csv_list'].append('')
        self.tab_widget.addTab(table, u'tab')
        self.tab_widget.setCurrentIndex(self.tab_widget.count() - 1)

    def _add_tab_launch(self):
        table = self._make_table_widget()
        table.cellChanged.connect(self._update_current_table_array)
        self.tab_list.append(table)
        #self.pcc_pref['csv_list'].append('')
        self.tab_widget.addTab(table, u'tab')
        self.tab_widget.setCurrentIndex(self.tab_widget.count() - 1)

    def _del_tab(self):
        index = self.tab_widget.currentIndex()

        if (self.tab_widget.count() > 1):
            self.tab_widget.removeTab(index)
            self.tab_list.pop(index)
            self.pcc_pref['csv_list'].pop(index)

        self._save_pref_json()

    def _update_current_table_array(self):
        index = self.tab_widget.currentIndex()
        self.current_table = self.tab_list[index]
        self.current_table_array = read_table(self.current_table)

        # update csv path line
        self.csv_line.setText(self.pcc_pref['csv_list'][index])

    def _get_file_name(self):
        file_path = self.csv_line.text()
        file_name, ext = os.path.splitext(os.path.basename(file_path))

        return file_name

    #--------------------------------------------------------------------------
    # table
    #--------------------------------------------------------------------------
    def _addRowButton_onClicked(self):
        self.current_table.insertRow(self.current_table.rowCount())

    def _delRowButton_onClicked(self):
        self.current_table.removeRow(self.current_table.rowCount() - 1)

    def _insRowButton_onClicked(self):
        if not self.current_table.currentRow() == -1:
            self.current_table.insertRow(self.current_table.currentRow())

    def _delSelButton_onClicked(self):
        if not self.current_table.currentRow() == -1:
            self.current_table.removeRow(self.current_table.currentRow())

    def _make_table_widget(self):
        table_widget = QTableWidget()
        header_labels = [
                "CC",
                "Connect",
                "Scale",
                "Offset (0.0-1.0)",
                "Attr Initial",
                "Attribute"
                ]
        table_widget.setColumnCount(len(header_labels))
        table_widget.setHorizontalHeaderLabels(header_labels)
        table_widget.verticalHeader().setVisible(False)

        try:
            table_widget.horizontalHeader().setSectionResizeMode(
                    QHeaderView.Interactive)

        except:
            table_widget.horizontalHeader().setResizeMode(
                    QHeaderView.Interactive)

        table_widget.setAlternatingRowColors(True)
        table_widget.horizontalHeader().setStretchLastSection(True)
        data_list = [["1", "0", "1", "0.5", "0", "pCube1.tx"]]
        table_widget.setRowCount(len(data_list))

        for row, col_data in enumerate(data_list):
            for col, value in enumerate(col_data):
                item = QTableWidgetItem(value)
                table_widget.setItem(row, col, item)

        return table_widget

def read_table(table):
    table_data = []

    for r in xrange(table.rowCount()):
        cal_data = []

        for c in xrange(table.columnCount()):
            data = table.item(r, c)

            if (data is not None):
                if c == 0 or c == 1:

                    # cc, connect
                    cal_data.append(int(data.text()))
                elif c > 1 and c < 5:

                    # scale, offset, attr initial
                    cal_data.append(float(data.text()))
                else:

                    # attribute name
                    cal_data.append(data.text())

        table_data.append(cal_data)

    return table_data

def exec_pcc(arg):
    #print 'Recieved: ', arg

    # split at 'start' and 'end'
    arg = filter(lambda w: len(w) > 0, re.split('start,|,end', arg))
    #print arg
    msg_list = []

    for m in arg:
        m = m.split(',')
        msg_list.append(m)

    #print msg_list
    '''
    msg_list
      m[0](cc): 0 - 128
      m[1](value): 0.0 - 1.0

    g_pcc.current_table_array
      colm[0]:cc
      colm[1]:connect
      colm[2]:scale
      colm[3]:slider offset value
      colm[4]:attribute initial value
      colm[5]:attribute name
    '''

    # fader
    for m in msg_list:
        for colm in g_pcc.current_table_array:

            # not a blank row and connect true
            if (len(colm) == 6) and colm[1] == 1:

                if int(m[0]) == colm[0]:

                    # match cc
                    offset = float(m[1]) - colm[3]
                    cmds.setAttr(colm[5], colm[4] + (offset * colm[2]))
                elif int(m[0]) == colm[0] + 20:

                    # m[0]がCC+20だったらアトリビュートにキーを打つ
                    # if m[0] == CC+20 then set keyframe for attribute
                    cmds.setKeyframe(colm[5])

    # Display CC number
    g_pcc.cc_lcd.display(msg_list[0][0])

    # Playback and tab control
    if msg_list[0][0] == '41' and msg_list[0][1] == '1':
        cmds.play(forward=True)
    elif msg_list[0][0] == '42' and msg_list[0][1] == '1':
        cmds.play(state=False)
    elif msg_list[0][0] == '43' and msg_list[0][1] == '1':
        mel.eval('playButtonStepBackward;')
    elif msg_list[0][0] == '44' and msg_list[0][1] == '1':
        mel.eval('playButtonStepForward;')
    elif msg_list[0][0] == '61' and msg_list[0][1] == '1':

        # previous tab
        tabCount = g_pcc.tab_widget.count()
        tabIndex = g_pcc.tab_widget.currentIndex()

        if tabIndex == 0:
            g_pcc.tab_widget.setCurrentIndex(tabCount - 1)
        else:
            g_pcc.tab_widget.setCurrentIndex(tabIndex - 1)


    elif msg_list[0][0] == '62' and msg_list[0][1] == '1':

        # next tab
        tabCount = g_pcc.tab_widget.count()
        tabIndex = g_pcc.tab_widget.currentIndex()

        if tabIndex == tabCount - 1:
            g_pcc.tab_widget.setCurrentIndex(0)
        else:
            g_pcc.tab_widget.setCurrentIndex(tabIndex + 1)

def main():
    global g_pcc

    g_pcc = PccUI()
    g_pcc._load_pref_json()
    g_pcc._check_port()
    g_pcc.show()

    return g_pcc

if __name__ == '__main__':
    main()
