# %%
from build123d import *
from ocp_vscode import *
from inspect import currentframe as cf

set_port(3939)
show_clear()
set_defaults(ortho=True, default_edgecolor="#121212")
# %%


with BuildPart() as p:
    with BuildSketch() as s:
        RectangleRounded(125, 150, 10)
    extrude(amount=20 / 2, both=True)

    edgs = faces().sort_by(Axis.Z)[-1].edges().group_by(Axis.Y)[0:3]

    with BuildSketch(Plane.XZ.offset(0)) as s:
        Trapezoid(100, 10, 45, align=(Align.CENTER, Align.MIN))
    extrude(amount=-100, mode=Mode.SUBTRACT)

    chamfer(edgs, 8)

    with BuildSketch(Plane.XY.offset(20 / 2)) as s:
        with Locations((0, -50)):
            Text("sharp123", 15)
    extrude(amount=-3, mode=Mode.SUBTRACT)


# print(f"\npart mass = {p.part.volume*densa}")
classes = (BuildPart, BuildSketch, BuildLine)  # for OCP-vscode
set_colormap(ColorMap.seeded(colormap="rgb", alpha=1, seed_value="vscod"))
variables, s_o, s_n, slocal = (list(cf().f_locals.items()), [], [], False)
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
    edgs,
    names=s_n,
    reset_camera=Camera.KEEP,
)
