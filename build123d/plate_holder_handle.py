# %%
from build123d import *
from ocp_vscode import *
from inspect import currentframe as cf

set_port(3939)
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

    with BuildSketch(Plane.YZ.offset(0)) as s:
        Trapezoid(2.5 * 25, 30, 80, align=(Align.CENTER, Align.MIN))
        vtxs2 = vertices().group_by(Axis.Y)[-1]
        fillet(vtxs2, 15)
    extrude(amount=18 / 2, both=True, mode=Mode.INTERSECT)
    newe = edges(Select.NEW)
    fillet(newe, 0.5)
    mirror(about=Plane.YZ)

    with BuildSketch(Plane.XZ.offset(0)) as s:
        with Locations((0, 6)):
            Circle(8 / 2)
    extrude(amount=100, mode=Mode.SUBTRACT)

    newe2 = edges(Select.NEW)
    chamfer(newe2, 0.5)

# print(f"\npart mass = {p.part.volume*densa}")
classes = (BuildPart, BuildSketch, BuildLine)  # for OCP-vscode
set_colormap(ColorMap.seeded(colormap="rgb", alpha=1, seed_value="vscod"))
variables, s_o, s_n, slocal = (list(cf().f_locals.items()), [], [], True)
for name, obj in variables:
    if (
        isinstance(obj, classes)
        and not name.startswith("_")
        and not name.startswith("obj")
        and not obj._obj is None
    ):
        if obj._obj_name != "sketch" or slocal:
            s_o.append(obj), s_n.append(f"{name}.{obj._obj_name}")
        elif obj._obj_name == "sketch":
            s_o.append(obj.sketch), s_n.append(f"{name}.{obj._obj_name}")
show(
    *s_o,
    vtxs,
    newe,
    names=s_n,
    reset_camera=Camera.KEEP,
)
