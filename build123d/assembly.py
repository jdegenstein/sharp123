# %%
from build123d import *
from ocp_vscode import *

show_clear()
set_defaults(ortho=True, default_edgecolor="#121212")

# %%

from angle_adjustment_nut import p_angle_nut
from angle_adjustment_screw import p_angle_screw
from base_plate import p_base_plate
# from clamp_arm import p_clamp # TODO: debug why this is not working
from clamp_arm_holder import p_clamp_arm_holder
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
        p_base_plate.part,
        # p_clamp.part,
        p_clamp_arm_holder.part,
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




set_colormap(ColorMap.golden_ratio())
# fmt: off
show_all(
    classes = [BuildPart, BuildSketch, BuildLine, ],  # comment to show all objects
    include = ["packed", ],
    exclude = ["", ],
    show_sketch_local = False,
    helper_scale = 1,  # controls size of e.g. planes and axes
)  # fmt: on
