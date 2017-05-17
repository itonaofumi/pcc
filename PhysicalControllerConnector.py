# -*- coding: utf-8 -*-
import maya.cmds as mc
import maya.mel as mm
import os
import os.path
import csv
import re

def start():
    is_exists_window = mc.window('pccWindow', q=True, exists=True)
    if is_exists_window:
        mc.deleteUI('pccWindow')
        create_window()
    else:
        create_window()

def create_window():

    def edit_cell(row, column, value):
        return 1

    def add_row(*args):
        last_row_num = mc.scriptTable('table', query=True, rows=True)
        mc.scriptTable('table', edit=True, insertRow=last_row_num)

    def delete_row(*args):
        last_row_num = mc.scriptTable('table', query=True, rows=True)
        mc.scriptTable('table', edit=True, deleteRow=last_row_num - 1)

    def insert_add_row(*args):
        try:
            selected_row = mc.scriptTable('table', query=True,
                    selectedRows=True)[0]
            if selected_row == None:
                print 'Select Row to Insert'
            else:
                mc.scriptTable('table', edit=True, insertRow=selected_row)
        except:
            print 'Select Row to Insert'

    def delete_sel_row(*args):
        try:
            selected_row = mc.scriptTable('table', query=True, 
                    selectedRows=True)[0]
            if selected_row == None:
                print 'Select Row to Delete'
            else:
                mc.scriptTable('table', edit=True, deleteRow=selected_row)
        except:
            print 'Select Row to Delete'
  
    def open_port():
        port_name = 'pcc:' + mc.textFieldButtonGrp('portField',
                q=True, text=True)
        is_port_open = mc.commandPort(port_name, query=True)
        if not is_port_open:
            melproc = """
            global proc portData(string $arg){
                python(("pcc.exec_pcc(\\"" + $arg + "\\")"));
            }
            """
            mm.eval(melproc)

            mc.commandPort(name=port_name, echoOutput=False, noreturn=False,
                    prefix="portData")


    # 起動時にprefファイルを読み込み、最後に読み込んだcsvパスを調べる
    pref_path = os.path.expanduser('~') + '/pcc.pref'
    csv_path = os.path.expanduser('~') + '/pcc.csv'

    if (mc.file(pref_path, query=True, exists=True)):
        # prefファイルがあるなら読み込む
        csv_path = load_pref(pref_path)
        print 'Load pref file', csv_path

    window = mc.window('pccWindow', widthHeight=(750, 450),
            title='Physical Controller Connector', menuBar=True)

    form = mc.formLayout()

    port_layout = mc.rowLayout(numberOfColumns=3,
            ct3=['left', 'left', 'left'],
            co3=[0, 425, 0])
    mc.textFieldButtonGrp('portField', label='Port:', text='3000',
            buttonLabel='Open', cw3=[30, 50, 50], bc=open_port)
    mc.textFieldGrp('trackNum', editable=False, label='Track:',
            text=_track_num, columnWidth2=[100, 20])
    mc.textFieldGrp('ccNum', editable=False, label='CC:',
            text=_cc_num, columnWidth2=[30, 20])
    mc.setParent('..')

    global _track_num
    global _cc_num
    file_layout = mc.rowLayout(numberOfColumns=3)
    open_button = mc.iconTextButton(style='iconOnly', image1='fileOpen.png',
            command=load_csv)
    save_buton = mc.iconTextButton(style='iconOnly', image1='fileSave.png',
            command=save_csv)
    mc.textField('selectCsv', text=csv_path, width=500)
    mc.setParent('..')

    util_layout = mc.rowLayout(numberOfColumns=1)
    mc.button(label='Insert Select Attr', width=120, command=set_cell)
    mc.setParent('..')

    table =  mc.scriptTable('table', rows=8, columns=7,
            columnWidth=(
                [1, 50], [2, 50], [3, 50], [4, 50], [5, 100], [6, 100], [7, 300]
                ),
            label=[
                (1, 'Track'), (2, 'CC'), (3, 'Connect'), (4, 'Scale'),
                (5, 'Offset (0.0-1.0)'), (6, 'Attr Initial'), (7, 'Attribute')
                ],
            cellChangedCmd=edit_cell)

    add_button = mc.button(label='Add Row', command=add_row)
    delete_button = mc.button(label='Delete Row', command=delete_row)
    ins_add_row_button = mc.button(label='Insert to Selected Row',
            command=insert_add_row)
    del_sel_row_button = mc.button(label='Delete Selected Row',
            command=delete_sel_row)
  
    mc.formLayout(form, edit=True, 
        attachForm=[
            (port_layout, 'top', 5),
            (port_layout, 'left', 5),
            (file_layout, 'top', 5),
            (file_layout, 'left', 5),
            (util_layout, 'top', 0),
            (util_layout, 'left', 5),
            (table, 'top', 0),
            (table, 'left', 5),
            (table, 'right', 5),
            (table, 'bottom', 0),
            (add_button, 'left', 0),
            (add_button, 'bottom', 0), 
            (delete_button, 'bottom', 0),
            (delete_button, 'right', 0),
            (ins_add_row_button, 'bottom', 0),
            (ins_add_row_button, 'right', 0),
            (del_sel_row_button, 'bottom', 0),
            (del_sel_row_button, 'right', 0)
            ],
        attachControl=[
            (file_layout, 'top', 5, port_layout),
            (util_layout, 'top', 5, file_layout),
            (table, 'top', 5, util_layout),
            (table, 'bottom', 0, add_button), 
            ],
        attachPosition=[
            (add_button, 'right', 0, 25),
            (delete_button, 'left', 0, 25),
            (delete_button, 'right', 0, 50),
            (ins_add_row_button, 'left', 0,50),
            (ins_add_row_button, 'right', 0, 75),
            (del_sel_row_button, 'left', 0,75)], 
        attachNone=[
            (add_button, 'top'),
            (delete_button, 'top'),
            (ins_add_row_button, 'top'),
            (del_sel_row_button, 'top')]
        )
  
    mc.showWindow(window)
    
    # 最後に読み込んだcsvを読み込み
    exec_load(csv_path)


def load_csv():
    csv_path = mc.textField('selectCsv', query=True, text=True)
    file_filter = '*.csv'
    import_file_name = mc.fileDialog2(fileMode=1, fileFilter=file_filter,
            dialogStyle=2, startingDirectory=csv_path,
            caption='Select CSV file')
    if import_file_name:
        exec_load(import_file_name[0])


def exec_load(csv_path):
    mc.textField('selectCsv', edit=True, text=csv_path)

    delete_all_rows()

    o_file = open(csv_path, 'r')
    reader = csv.reader(o_file)
    header = next(reader)
  
    row_no = 1  # 最初の行はスキップするため、１からスタート
    for r in reader:
        # 一行ずつ行を追加し、読み込んだcsvを書き込み
        mc.scriptTable('table', edit=True, insertRow=row_no)
        mc.scriptTable('table', cellIndex=(row_no, 1), edit=True,
                cellValue=r[0])
        mc.scriptTable('table', cellIndex=(row_no, 2), edit=True,
                cellValue=r[1])
        mc.scriptTable('table', cellIndex=(row_no, 3), edit=True,
                cellValue=r[2])
        mc.scriptTable('table', cellIndex=(row_no, 4), edit=True, 
                cellValue=r[3])
        mc.scriptTable('table', cellIndex=(row_no, 5), edit=True, 
                cellValue=r[4])
        mc.scriptTable('table', cellIndex=(row_no, 6), edit=True, 
                cellValue=r[5])
        mc.scriptTable('table', cellIndex=(row_no, 7), edit=True, 
                cellValue=r[6])
        row_no = row_no + 1
    o_file.close()

    save_pref(mc.textField('selectCsv', query=True, text=True))


def delete_all_rows():
    total_rows = mc.scriptTable('table', query=True, rows=True)
    for r in range(total_rows):
        if not r == 0:
            mc.scriptTable('table', edit=True, deleteRow=1)
 

def save_csv():
    o_file = mc.textField('selectCsv', query=True, text=True)
  
    if not (mc.file(o_file, query=True, exists=True)):
        tmp_csv_file = open(o_file, 'w', os.O_CREAT)
    else:
        tmp_csv_file = open(o_file, 'w')
  
    writer = csv.writer(tmp_csv_file, lineterminator='\n')
    all_rows = mc.scriptTable('table', query=True, rows=True)
  
    for o_r in range(all_rows):
        all_colums = mc.scriptTable('table', query=True, columns=True)
        data_list = []
        for o_c in range(all_colums - 1):
            if o_r == 0:
                data_list = ['Track', 'CC', 'Connect', 'Scale', 'Offset',
                        'Attr Initial', 'Attribute']
            else:
                cell_list = mc.scriptTable('table', cellIndex=(o_r, o_c + 1),
                        query=True, cellValue=True)
                if type(cell_list) == list:
                    cell_text = ''.join(cell_list)
                elif cell_list == None:
                    cell_text = u''
                else:
                    cell_text = cell_list
                data_list.append(cell_text)
        writer.writerow(data_list)
    tmp_csv_file.close()
    print 'save csv'

    save_pref(mc.textField('selectCsv', query=True, text=True))


def load_pref(pref_path):
    o_file = open(pref_path, 'r')
    for line in o_file:
        return line
    o_file.close()


def save_pref(csv_path):
    o_file = os.path.expanduser('~') + '/pcc.pref'
    if not (mc.file(o_file, query=True, exists=True)):
        prefFile = open(o_file, 'w', os.O_CREAT)
    else:
        prefFile = open(o_file, 'w')
    prefFile.write(csv_path)
    prefFile.close()


def set_cell(arg):
    selected_objects = mc.ls(selection=True)
    selected_channels = mc.channelBox('mainChannelBox', q = True,
            selectedMainAttributes = True)
    attr = selected_objects[0] + '.' + selected_channels[0]
    #print selected_objects
    #print selected_channels
    #print attr 

    selected_row = mc.scriptTable('table', q=True, selectedRow=True)

    mc.scriptTable('table', cellIndex=(selected_row, 7), edit=True,
            cellValue=attr)


def read_table():
    all_rows = mc.scriptTable('table', query=True, rows=True)
    data_list = []
    for r in range(all_rows):
        if not r == 0:  # 最初の行は空なのでスキップする
            all_colums = mc.scriptTable('table', query=True, columns=True)
            row_list = []
            for c in range(all_colums - 1):
                if not r == 0:  # 最初のカラムは空なのでスキップする
                    cell_list = mc.scriptTable('table', cellIndex=(r, c + 1),
                            query=True, cellValue=True)
                    row_list.append(cell_list[0])
            data_list.append(row_list)
    return data_list


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
    #print table
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

    ''' auto keyframe is very heavy...
    # toggle auto keyframe
    if msg_list[0][0] == '45' and msg_list[0][1] == '1':
        if mc.autoKeyframe(q=True, state=True) == True:
            mc.autoKeyframe(state=False)
        else:
            mc.autoKeyframe(state=True)
    '''


'''
def get_selected_cells():
    cells = mc.scriptTable('table', query=True, selectedCells=True)
    if not cells is None:
        rows = [] # 行番号だけ抜き出し
        cell_list = [] # 行、列の順で取り出し

        if len(cells) > 2: # 複数cell選択状態
            cell = []
            count = 0
            for c in cells:
                if count == 0: # 行番号だけ取り出し
                    rows.append(c)

                cell.append(c)
                count += 1

                if count == 2: 
                    # 次のcellなので、これまでの値を配列に格納し、
                    # カウンターをリセット
                    cell_list.append(cell)
                    cell = []
                    count = 0
        else: # 1cell選択状態
            rows.append(cells[0])
            cell_list = cells

        return rows, cell_list
'''
