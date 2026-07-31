# %%
from build123d import *
from ocp_vscode import *

show_clear()
set_defaults(ortho=True, default_edgecolor="#121212")

from sharp123 import (
    create_assembly_config,
    DebugMixin,
    Tower,
    BasePlate,
    ClampArmHolder,
    ClampingScrew,
    TaperedClampingNut,
    LongPin,
    PlateHandleShaft,
    Washer,
    ClampArm,
)

# tower angle nut
# # from clamp_arm import p_clamp # TODO: debug why this is not working
# from diamond_plate_holder import p_diamond_plate_holder
# from plate_holder_handle import p_plate_handle


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
    # TODO: fix this hacky stuff:
    from IPython import get_ipython

    ipython = get_ipython()
    if ipython is not None:
        ipython.run_line_magic("load_ext", "autoreload")
        ipython.run_line_magic("autoreload", "3")
    else:
        print("Not running in an IPython environment.")
    # %reset -f

    par = create_assembly_config()
    tower = Tower(par)
    # tower.show_debug(render_joints=True)

    base_plate = BasePlate(par)
    # base_plate.show_debug(render_joints=True)

    clamp_arm_holder = ClampArmHolder(par)
    # clamp_arm_holder.show_debug(render_joints=True)

    clamping_screw = ClampingScrew(par)
    # clamping_screw.show_debug(render_joints=True)

    clamping_screw = ClampingScrew(par)
    # clamping_screw.show_debug(render_joints=True)

    tapered_clamping_nut = TaperedClampingNut(par)
    # tapered_clamping_nut.show_debug(render_joints=True)

    long_pin_1 = LongPin(par)
    # long_pin_1.show_debug(render_joints=True)

    long_pin_2 = LongPin(par)
    # long_pin_2.show_debug(render_joints=True)

    clamp_arm = ClampArm(par)
    # clamp_arm.show_debug(render_joints=True)

    clamp_arm_mirror = clamp_arm.solid()

    # TODO: find a better way to mirror and preserve joints
    clamp_arm_mirror = mirror(clamp_arm_mirror, about=Plane.XZ.offset(0))
    RigidJoint(
        "j1", to_part=clamp_arm_mirror, joint_location=clamp_arm.joints["j1"].location
    )

    ############# ASSEMBLE JOINTS #######################
    base_plate.joints["j1"].connect_to(tower.joints["j1"])
    tower.joints["j2"].connect_to(clamp_arm_holder.joints["j1"])
    clamp_arm_holder.joints["j2"].connect_to(clamping_screw.joints["j1"])
    clamp_arm_holder.joints["j3"].connect_to(long_pin_1.joints["j1"])
    clamp_arm_holder.joints["j4"].connect_to(long_pin_2.joints["j1"])
    clamping_screw.joints["j2"].connect_to(tapered_clamping_nut.joints["j1"])
    long_pin_1.joints["j2"].connect_to(clamp_arm.joints["j1"])
    long_pin_2.joints["j2"].connect_to(clamp_arm_mirror.joints["j1"])

    ############# APPLY MATERIALS and SHOW ###############
    from bd_materials import plastics, processes

    tower.material = plastics.asa(color="teal", process=processes.fdm(mm_per_uv=0.3))
    base_plate.material = plastics.asa(
        color="salmon", process=processes.fdm(mm_per_uv=0.3)
    )
    clamp_arm_holder.material = plastics.asa(
        color="steelblue", process=processes.fdm(mm_per_uv=0.3)
    )
    clamping_screw.material = plastics.asa(
        color="chartreuse", process=processes.fdm(mm_per_uv=0.3)
    )
    # for solid in clamping_screw.solids():
    # solid.material = plastics.asa(color="chartreuse", process=processes.fdm(mm_per_uv=.5))
    show_all(render_joints=True)
