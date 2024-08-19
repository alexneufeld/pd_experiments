import os
import FreeCAD
import FreeCADGui
from freecad.pd_features import ICONPATH
from .centerdrill import CenterDrill
from .viewprovider_centerdrill import ViewProviderCenterDrill
from .task_centerdrill import CenterDrillTaskPanel
from .gui_utils import get_active_body


class AddCenterDrillCommand:

    def GetResources(self):
        return {
            "Pixmap": os.path.join(ICONPATH, "CenterDrill.svg"),
            "Menutext": "AddCenterDrillCommand",
            "tooltip": "Add a center drill to the body",
        }

    def Activated(self):
        doc = FreeCAD.ActiveDocument
        active_body = get_active_body()
        obj = doc.addObject("PartDesign::FeatureSubtractivePython","CenterDrill")
        active_body.addObject(obj)
        CenterDrill(obj)
        ViewProviderCenterDrill(obj.ViewObject)
        # assign the selected reference geometry
        sel = FreeCADGui.Selection.getSelection()
        if not (len(sel) == 1) and (sel[0].TypeId == "Sketcher::SketchObject"):
            print("Select exactly one sketch object in the active body")  # change this to be more consistent with base partdesign stuff
            return
        taskpanel = CenterDrillTaskPanel(obj, True)
        FreeCADGui.Control.showDialog(taskpanel)

    def IsActive(self):
        return FreeCADGui.ActiveDocument is not None
