# %%
from build123d import *
from ocp_vscode import *

show_clear()
set_defaults(ortho=True, default_edgecolor="#121212")
# %%

# TODO: add parameterization and validate parameters against other models


with BuildPart() as p_plate_handle:
    with BuildSketch(Plane.XZ.offset(0)) as s:
        Trapezoid(18, 30, 85, align=(Align.CENTER, Align.MIN))
        split(bisect_by=Plane.YZ)
        with Locations((8, 22)):
            Circle(4, mode=Mode.SUBTRACT)
        with Locations((10, 14)):
            Circle(6, mode=Mode.SUBTRACT)
        vtxs = vertices().sort_by(Axis.X)[-5:-1]
        fillet(vtxs, 2)
    extrude(amount=2.5 * 25 / 2, both=True)

    with BuildSketch(Plane.YZ.offset(0)) as s2:
        Trapezoid(2.5 * 25, 30, 80, align=(Align.CENTER, Align.MIN))
        vtxs2 = vertices().group_by(Axis.Y)[-1]
        fillet(vtxs2, 12)
    extrude(amount=14, both=True, mode=Mode.INTERSECT)
    # newe = edges(Select.NEW).group_by(Axis.X)[1::] # TODO: fix fillet
    # fillet(newe, 0.01)
    mirror(about=Plane.YZ)

    with BuildSketch(Plane.XZ.offset(0)) as s3:
        with Locations((0, 6)):
            Circle(8 / 2)
    extrude(amount=100, mode=Mode.SUBTRACT)

    newe2 = edges(Select.NEW)
    chamfer(newe2, 0.5)

show_all()