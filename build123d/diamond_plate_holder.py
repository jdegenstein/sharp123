# %%
from build123d import *
from ocp_vscode import *
from inspect import currentframe as cf

set_port(3939)
show_clear()
set_defaults(ortho=True, default_edgecolor="#121212")
# %%

# Diamond Plate Product Dimensions	3.25"L x 2.0"W x 1/16"H

plate_len = 3.25 * IN + 0.4
plate_wid = 2.0 * IN + 0.4
plate_th = 1 / 16 * IN * 0.8

holder_th = 5

# TODO: more parameterization

with BuildPart() as p_diamond_plate_holder:
    with BuildSketch() as s:
        Rectangle(plate_len, plate_wid)
        offset(amount=4)
    extrude(amount=holder_th)
    with BuildSketch(faces().sort_by(Axis.Z)[-1]) as s:
        Rectangle(plate_len, plate_wid)
    extrude(amount=-plate_th, mode=Mode.SUBTRACT)

    with Locations((0, -15)):
        Hole(16 / 2)

    with Locations(Plane.XY.offset(4 - plate_th)):
        with GridLocations(plate_len * 0.8, 1, 2, 1):
            CounterBoreHole(5 / 2, 10.5 / 2, 1)


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
    # ,
    names=s_n,
    reset_camera=Camera.KEEP,
)
