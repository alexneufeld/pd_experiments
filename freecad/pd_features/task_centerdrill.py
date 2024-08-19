import os
import FreeCAD
import FreeCADGui
try:
    from PySide import QtCore
    from PySide import QtGui
    from PySide import QtWidgets
except ImportError:
    from PySide2 import QtCore
    from PySide2 import QtGui
    from PySide2 import QtWidgets
from freecad.pd_features import ICONPATH



class CenterDrillTaskPanel:
    def __init__(self, feature, isNewFeature):
        self.feature = feature
        self.isNewFeature = isNewFeature
        self.doc = FreeCAD.ActiveDocument
        self.guidoc = FreeCADGui.ActiveDocument
        uiPath = os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "TaskCenterDrillParameters.ui"
        )
        loader = FreeCADGui.UiLoader()
        self.form = loader.load(uiPath)
        self.setupUI()
        self.doc.openTransaction("Edit Center Drill")
        FreeCADGui.Selection.clearSelection()

    def setupUI(self):
        # set window title and icon
        self.form.setWindowTitle("Center Drill Parameters")
        self.form.setWindowIcon(QtGui.QIcon(os.path.join(ICONPATH, "CenterDrill.svg")))

        self.updateUI()

    def updateUI(self):
        # enable/disable UI fields based on object state
        pass

    def getStandardButtons(self):
        return int(QtGui.QDialogButtonBox.Cancel | QtGui.QDialogButtonBox.Ok)

    def accept(self):
        self.doc.commitTransaction()
        self.guidoc.resetEdit()
        FreeCADGui.Control.closeDialog()
        self.doc.recompute()

    def reject(self):
        self.doc.abortTransaction()
        FreeCADGui.Control.closeDialog()
        # delete the object if it was just created
        if self.isNewFeature:
            self.doc.removeObject(self.feature.Name)
        self.doc.recompute()

    def focusUiStart(self):
        # start_widget = self.form.ADDME
        # start_widget.setFocus()
        # start_widget.selectAll()
        pass
