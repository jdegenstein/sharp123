# %%
from build123d import *
from ocp_vscode import *

show_clear()
set_defaults(ortho=True, default_edgecolor="#121212")

from sharp123 import create_assembly_config, Tower, BasePlate

# from angle_adjustment_nut import p_angle_nut
# from angle_adjustment_screw import p_angle_screw
# from base_plate import p_base_plate
# # from clamp_arm import p_clamp # TODO: debug why this is not working
# from clamp_arm_holder import p_clamp_arm_holder
# from clamping_screw import p_angle_screw as p_clamp_screw
# from diamond_plate_holder import p_diamond_plate_holder
# from main_tower import p_tower
# from plate_holder_handle import p_plate_handle
# from small_parts import p_short_pin, p_long_pin, p_shaft, p_washer
# from tapered_clamping_nut import p_tapered_clamping_nut


# # %%

# packed = pack(
#     [
#         p_angle_nut.part,
#         p_angle_screw.part,
#         p_base_plate.part,
#         # p_clamp.part,
#         p_clamp_arm_holder.part,
#         p_clamp_screw.part,
#         p_diamond_plate_holder.part,
#         p_plate_handle.part,
#         p_tower.part,
#         p_short_pin.part,
#         p_long_pin.part,
#         p_shaft.part,
#         p_washer.part,
#         p_tapered_clamping_nut.part,
#     ],
#     padding=5,
#     align_z=True,
# )

if __name__ == "__main__":
    par = create_assembly_config()
    tower = Tower(par)
    tower.show_debug(render_joints=True)
    base_plate = BasePlate(par)
    base_plate.show_debug(render_joints=True)

    base_plate.joints["j1"].connect_to(tower.joints["j1"])
    # tower.joints["j1"].connect_to(base_plate.joints["j1"])

    show(tower,base_plate,render_joints=True)
    # set_colormap(ColorMap.golden_ratio())
    # # fmt: off
    # show_all(
    #     classes = [BuildPart, BuildSketch, BuildLine, ],  # comment to show all objects
    #     include = ["tower", ],
    #     exclude = ["", ],
    #     show_locals = False,
    #     helper_scale = 1,  # controls size of e.g. planes and axes
    # )  # fmt: on
