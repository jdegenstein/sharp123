from build123d import *
from ocp_vscode import *
from inspect import currentframe as cf

set_port(3939)
show_clear()
set_defaults(ortho=True, default_edgecolor="#121212")
# %%
from angle_adjustment_nut import p_angle_nut
from angle_adjustment_screw import p_angle_screw
from base_plate import p as base_plate  # TODO: Fixme
from clamp_arm import p_clamp
from clamp_arm_holder import p as clamp_arm_holder
from clamping_screw import p_angle_screw as p_clamp_screw
from diamond_plate_holder import p_diamond_plate_holder
from main_tower import p_tower
from plate_holder_handle import p_plate_handle
from small_parts import p_short_pin, p_long_pin, p_shaft, p_washer
from tapered_clamping_nut import p_tapered_clamping_nut


# %%

packed = pack(
    [
        p_angle_nut.part,
        p_angle_screw.part,
        base_plate.part,
        p_clamp.part,
        clamp_arm_holder.part,
        p_clamp_screw.part,
        p_diamond_plate_holder.part,
        p_plate_handle.part,
        p_tower.part,
        p_short_pin.part,
        p_long_pin.part,
        p_shaft.part,
        p_washer.part,
        p_tapered_clamping_nut.part,
    ],
    padding=5,
    align_z=True,
)


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
    packed,
    names=s_n,
    reset_camera=Camera.KEEP,
)
