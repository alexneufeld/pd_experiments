import FreeCAD
import Part


available_norms = [
    "DIN 333 Type A",
    "DIN 333 Type B",
    "DIN 333 Type R",
    "ASME B94.11M Plain Type",
    "ASME B94.11M Bell Type",
    "ISO 866",
    "ISO 2541",
]

available_sizes_per_norm = {
    "DIN 333 Type A": [
        "5.0 mm",
    ],
    "DIN 333 Type B": [
        "5.0 mm",
    ],
    "DIN 333 Type R": [
        "0.5 mm",
        "0.8 mm",
        "1.0 mm",
        "1.25 mm",
        "1.6 mm",
        "2.0 mm",
        "2.5 mm",
        "3.15 mm",
        "4.0 mm",
        "5.0 mm",
        "6.3 mm",
        "8.0 mm",
        "10.0 mm",
        "12.5 mm",
        ],
    "ASME B94.11M Plain Type": [
        "No. 00",
        "No. 0",
        "No. 1",
        "No. 2",
        "No. 3",
        "No. 4",
        "No. 5",
        "No. 6",
        "No. 7",
        "No. 8",
    ],
    "ASME B94.11M Bell Type": [
        "No. 11",
        "No. 12",
        "No. 13",
        "No. 14",
        "No. 15",
        "No. 16",
        "No. 17",
        "No. 18",
    ],
    "ISO 866": [
        "0.5 mm",
        "0.63 mm",
        "0.8 mm",
        "1.0 mm",
        "1.25 mm",
        "1.6 mm",
        "2.0 mm",
        "2.5 mm",
        "3.15 mm",
        "4.0 mm",
        "5.0 mm",
        "6.3 mm",
        "8.0 mm",
        "10.0 mm",
    ],
    "ISO 2540": [
        "1.0 mm",
        "1.25 mm",
        "1.6 mm",
        "2.0 mm",
        "2.5 mm",
        "3.15 mm",
        "4.0 mm",
        "5.0 mm",
        "6.3 mm",
        "8.0 mm",
        "10.0 mm",
    ],
    "ISO 2541": [
        "1.0 mm",
        "1.25 mm",
        "1.6 mm",
        "2.0 mm",
        "2.5 mm",
        "3.15 mm",
        "4.0 mm",
        "5.0 mm",
        "6.3 mm",
        "8.0 mm",
        "10.0 mm",
    ],
}

iso_866_dimensions = {
    #           ┌───────────────── pilot diameter
    #           │     ┌─────────── pilot length
    #           │     │     ┌───── major diameter
    #           V     V     V
    "0.5 mm":  (0.5,  0.9,  1.06),
    "0.63 mm": (0.63, 1.05, 1.32),
    "0.8 mm":  (0.8,  1.3,  1.70),
    "1.0 mm":  (1.0,  1.6,  2.12),
    "1.25 mm": (1.25, 1.9,  2.65),
    "1.6 mm":  (1.6,  2.4,  3.35),
    "2.0 mm":  (2.0,  2.9,  4.25),
    "2.5 mm":  (2.5,  3.6,  5.30),
    "3.15 mm": (3.15, 5.4,  6.70),
    "4.0 mm":  (4.0,  5.6,  6.70),
    "5.0 mm":  (5.0,  6.9,  8.50),
    "6.3 mm":  (6.3,  8.6,  10.6),
    "8.0 mm":  (8.0,  10.8, 13.2),
    "10.0 mm": (10.0, 13.5, 17.0),
}


class SketchBasedPython:
    def __init__(self, obj):
        obj.Proxy = self

        # set up sketch based parameters to mimic normal partdesign features
        obj.addProperty(
            "App::PropertyLinkSub",
            "Profile",
            "SketchBased",
            "Reference to sketch",
        )
        obj.addProperty(
            "App::PropertyBool",
            "Midplane",
            "SketchBased",
            "Extrude symmetric to sketch face",
        )
        obj.addProperty(
            "App::PropertyBool",
            "Reversed",
            "SketchBased",
            "Reverse extrudion direction",
        )
        obj.addProperty(
            "App::PropertyLinkSub",
            "UpToFace",
            "SketchBased",
            "Face where feature will end",
        )
        obj.addProperty(
            "App::PropertyLinkSubList",
            "UpToShape",
            "SketchBased",
            "Shape where feature will end",
        )
        obj.addProperty(
            "App::PropertyBool",
            "AllowMultiFace",
            "SketchBased",
            "Allow multiple faces in profile",
        )


class CenterDrill(SketchBasedPython):
    def __init__(self, obj):
        super().__init__(obj)
        obj.Proxy = self
        # add_property(type, name, section, description)
        # supported properties
        obj.addProperty(
            "App::PropertyEnumeration",
            "Norm",
            "CenterDrill",
            "Standard to select drill size from",
        )
        obj.addProperty(
            "App::PropertyEnumeration",
            "Size",
            "CenterDrill",
            "Center Drill Nominal Size",
        )

        obj.Norm = available_norms

    def execute(self, obj):
        parent_shape = obj.BaseFeature.Shape
        if obj.Norm == "ISO 866":
            pilot_diameter, pilot_length, major_diameter = iso_866_dimensions[obj.Size]
            # create the basic shape
            p0 = FreeCAD.Vector(0.0, 0.0, 0.0)
            p1 = FreeCAD.Vector(major_diameter / 2.0, 0.0, 0.0)
            taper_len = 0.5 * (major_diameter - pilot_diameter)
            p2 = FreeCAD.Vector(
                pilot_diameter / 2.0,
                0.0,
                -1 * taper_len
            )
            p4 = FreeCAD.Vector(
                0.0,
                0.0,
                -1 * taper_len - pilot_length
            )
            p3 = p4 + FreeCAD.Vector(
                pilot_diameter / 2.0,
                0.0,
                0.5 * pilot_diameter * 0.57735  # tan(30)
            )
            lineset = [
                Part.makeLine(p0, p1),
                Part.makeLine(p1, p2),
                Part.makeLine(p2, p3),
                Part.makeLine(p3, p4),
                Part.makeLine(p4, p0),
            ]
            wire = Part.Wire(lineset)
            face = Part.makeFace(wire, "Part::FaceMakerSimple")
            revolved_shape = face.revolve(
                FreeCAD.Vector(0.0, 0.0, 0.0),
                FreeCAD.Vector(0.0, 0.0, 1.0),
                360
            )
            sketch_positions = [FreeCAD.Placement(edge.Curve.Center, edge.Curve.Rotation) for edge in obj.Profile[0].Shape.Edges]
            list_of_copies = [revolved_shape.transformed(vec.toMatrix()) for vec in sketch_positions]
            subtract_shape = Part.makeCompound(list_of_copies)
            obj.Shape = parent_shape.cut(subtract_shape)
            # obj.AddSubShape = Part.makeCompound(
            #     Part.Shape(),
            #     subtract_shape
            # )
            obj.AddSubShape = subtract_shape
        else:
            test_cyl = Part.makeCylinder(1.0, 2.0)
            obj.Shape = parent_shape.cut(test_cyl)



    def onChanged(self, obj, prop: str):
        if prop == "Norm":
            obj.Size = available_sizes_per_norm[obj.Norm]
        elif prop == "Size":
            pass

    def dumps(self):
        return {}

    def loads(self, state: dict):
        return None
