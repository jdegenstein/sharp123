# %%
from build123d import *
from ocp_vscode import *
from inspect import currentframe as cf

set_port(3939)
show_clear()
set_defaults(ortho=True, default_edgecolor="#121212")
# %%

# TODO: add parameterization, add splits and alignment pin holes, cross check dimensions against other parts

with BuildPart() as p:
    with BuildSketch() as s:
        Rectangle(100, 80, align=(Align.MIN, Align.CENTER))
        with Locations((10, 0)):
            Rectangle(100, 80 - 20, align=(Align.MIN, Align.CENTER), mode=Mode.SUBTRACT)
    extrude(amount=40 / 2, both=True)

    with BuildSketch(Plane.YZ.offset(0)) as s:
        RegularPolygon(20, 8, rotation=360 / 8 / 2, major_radius=False)
    extrude(amount=-60)

    edgs = faces().group_by(Axis.X)[-1].edges().filter_by(Axis.Y)
    chamfer(edgs, 40, 10)

    with Locations(Plane.XZ.offset(0)):
        with Locations((60, 10), (60, -10)):
            Hole(8 / 2)
        with Locations((35, 0)):
            Hole(15 / 2)

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
