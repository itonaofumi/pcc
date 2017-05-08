import maya.cmds as mc
import maya.mel as mm
import PhysicalControllerConnector as pcc

is_port_open = mc.commandPort('pcc:3000', query=True)
is_exists_window = mc.window('pccWindow', exists=True, q=True)

if not is_port_open:
    melproc = """
    global proc portData(string $arg){
        python(("pcc.exec_pcc(\\"" + $arg + "\\")"));
    }
    """
    mm.eval(melproc)

    mc.commandPort(name="pcc:3000", echoOutput=False, noreturn=False,
            prefix="portData")

    if not is_exists_window:
        pcc.create_window()
else:
    if not is_exists_window:
        pcc.create_window()
