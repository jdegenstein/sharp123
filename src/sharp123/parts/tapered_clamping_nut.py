# %%
from build123d import *
from ocp_vscode import *
from inspect import currentframe as cf

set_port(3939)
show_clear()
set_defaults(ortho=True, default_edgecolor="#121212")
# %%


from bd_warehouse import thread

mtt = thread.MetricTrapezoidalThread("14x3", 20, external=False)

# TODO: parameterize and validate sizes

with BuildPart() as p_tapered_clamping_nut:
    with BuildSketch() as s:
        SlotCenterPoint((0, 0), (10, 0), 25)
    extrude(amount=20, taper=5)
    split(bisect_by=Plane.YZ)
    with Locations((10, 0)):
        Hole(14 / 2)

mtt = Pos(10, 0) * mtt

assy_tapered_clamping_nut = Compound()
assy_tapered_clamping_nut.children = [p_tapered_clamping_nut.part, mtt]


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
    assy_tapered_clamping_nut,
    names=s_n,
    reset_camera=Camera.KEEP,
)
