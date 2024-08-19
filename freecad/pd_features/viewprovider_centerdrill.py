import os
import math
import FreeCAD
import FreeCADGui
from PySide import QtGui
from freecad.pd_features import ICONPATH
import pivy.coin as coin
from .task_centerdrill import CenterDrillTaskPanel


class ViewProviderCenterDrill:
    def __init__(self, vobj):
        vobj.Proxy = self
        pass

    def attach(self, vobj):
        pass

    def updateData(self, fp, prop):
        pass

    def getDisplayModes(self, obj):
        return []

    def onChanged(self, vp, prop):
        pass

    def getIcon(self):
        return os.path.join(ICONPATH, "CenterDrill.svg")

    def setEdit(self, vobj, mode=0):
        taskpanel = CenterDrillTaskPanel(vobj.Object, False)
        FreeCADGui.Control.showDialog(taskpanel)
        return True

    def unsetEdit(self, vobj, mode=0):
        FreeCADGui.Control.closeDialog()
        return False

    def doubleClicked(self, vobj):
        self.setEdit(vobj)
        return True

    def setupContextMenu(self, vobj, menu):
        action = menu.addAction(
            QtGui.QIcon(os.path.join(ICONPATH, "CenterDrill.svg")), "Edit Center Drill"
        )
        action.triggered.connect(lambda: self.setEdit(vobj))
        return False

    def dumps(self):
        return None

    def loads(self, state):
        return None
