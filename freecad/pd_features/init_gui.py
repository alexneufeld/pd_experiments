import os
import FreeCADGui
from freecad.pd_features.command_add_centerdrill import AddCenterDrillCommand

# Add the GUI commands
FreeCADGui.addCommand("CenterDrill_Add", AddCenterDrillCommand())


# This shouldn't need an entire workbench
class MorePDFeaturesWorkbench(FreeCADGui.Workbench):
    from freecad.pd_features import ICONPATH, TRANSLATIONSPATH
    from freecad.pd_features.TranslateUtils import translate

    MenuText = translate("More PD Features", "More PD Features")
    ToolTip = translate("More PD Features", "Add additional features to PartDesign bodies")
    Icon = os.path.join(ICONPATH, "WorkbenchIcon.svg")
    toolbox = []

    def GetClassName(self):
        return "Gui::PythonWorkbench"

    def Initialize(self):
        from freecad.pd_features import TRANSLATIONSPATH

        FreeCADGui.addLanguagePath(TRANSLATIONSPATH)
        FreeCADGui.updateLocale()
        self.appendMenu(
            "MORE_PD_FEATURES",
            [
                "CenterDrill_Add",
            ],
        )
        self.appendToolbar(
            "MORE_PD_FEATURES",
            [
                "CenterDrill_Add",
            ],
        )

    def Activated(self):
        pass

    def Deactivated(self):
        pass


FreeCADGui.addWorkbench(MorePDFeaturesWorkbench())
