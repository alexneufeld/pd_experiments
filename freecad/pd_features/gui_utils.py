import FreeCAD
import FreeCADGui


def get_active_body() -> FreeCAD.DocumentObject | None:
    active_body = None
    doc = FreeCAD.ActiveDocument
    guidoc = FreeCADGui.ActiveDocument
    if doc:
        # if there is an active body, use it
        active_body = guidoc.ActiveView.getActiveObject("pdbody")
        if active_body:
            return active_body
        # if there is only a single body in the document, use it
        list_of_bodies_in_document = [x for x in doc.Objects if x.TypeId == "PartDesign::Body"]
        if not list_of_bodies_in_document:
            return None
        if len(list_of_bodies_in_document) == 1:
            # active the body before using it
            guidoc.ActiveView.setActiveObject("pdbody",list_of_bodies_in_document[0])
            return list_of_bodies_in_document[0]
        else:  # more than one body, where all are inactive
            return None
    else:
        return None
