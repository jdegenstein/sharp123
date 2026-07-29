# %%
from build123d import *
from ocp_vscode import *
from inspect import currentframe as cf

set_port(3939)
show_clear()
set_defaults(ortho=True, default_edgecolor="#121212")
# %%

from bd_warehouse import thread

mtt_extern = thread.MetricTrapezoidalThread("14x3", 80, external=True)

# TODO: add parameterization

with BuildPart() as p_angle_screw:
    with BuildSketch() as s:
        Circle(11 / 2)
    extrude(amount=80)
    with BuildSketch() as s:
        Circle(14 / 2)
    extrude(amount=-7)
    with BuildSketch(faces().sort_by(Axis.Z)[-1]) as s:
        Circle(9 / 2)
    extrude(amount=7)
    topfe = faces().sort_by(Axis.Z)[-1].edges()
    chamfer(topfe, 1)
    with BuildSketch(faces().sort_by(Axis.Z)[0]) as s:
        Circle(20 / 2)
    extrude(amount=3)
    botf0 = faces().sort_by(Axis.Z)[0].edges()
    with BuildSketch(faces().sort_by(Axis.Z)[0]) as s_knob:
        RegularPolygon(40 / 2, 6)
        with Locations((vertices())):
            Circle(5, mode=Mode.SUBTRACT)
        fillet(vertices(), 1)
    extrude(amount=15)
    botf = faces().sort_by(Axis.Z)[0].edges()
    midf = faces().filter_by(Axis.Z).sort_by(Axis.Z)[1].outer_wire().edges()
    chamfer(botf, 1)
    chamfer(midf, 0.99)
    fillet(botf0, 2.5)

assy_angle_screw = Compound()
assy_angle_screw.children = [p_angle_screw.part, mtt_extern]


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
    mtt_extern,
    botf0,
    midf,
    assy_angle_screw,
    names=s_n,
    reset_camera=Camera.KEEP,
)
