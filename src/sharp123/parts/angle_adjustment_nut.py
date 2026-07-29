# %%
from build123d import *
from ocp_vscode import *
from inspect import currentframe as cf

set_port(3939)
show_clear()
set_defaults(ortho=True, default_edgecolor="#121212")
# %%

from bd_warehouse import thread

mtt = thread.MetricTrapezoidalThread("14x3", 15, external=False)

# TODO: add parameterization

with BuildPart() as p_angle_nut:
    with BuildSketch() as s:
        with Locations((0, 10)):
            Trapezoid(40, 25, 65, align=(Align.CENTER, Align.MAX))
        Circle(14 / 2, mode=Mode.SUBTRACT)
    extrude(amount=15)
    with BuildSketch(faces().sort_by(Axis.Y)[-1]) as s:
        Rectangle(5, 15)
    extrude(amount=15)
    holef = faces().filter_by(Axis.X).sort_by(Axis.X)[-1]
    with Locations(holef):
        Hole(10 / 2)
    newe = edges(Select.NEW)
    chamfer(newe, 2)

assy_angle_nut = Compound()
assy_angle_nut.children = [p_angle_nut.part, mtt]


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
    mtt,
    holef,
    newe,
    assy_angle_nut,
    names=s_n,
    reset_camera=Camera.KEEP,
)
