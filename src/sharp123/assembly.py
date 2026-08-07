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
    PlateHolderHandle,
    Washer,
    ClampArm,
    AngleAdjustmentScrew,
    AngleAdjustmentNut,
    DiamondPlateHolder,
    AAScrewKey,
    KnifeExample,
)

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

    angle_adjustment_screw = AngleAdjustmentScrew(par)
    # angle_adjustment_screw.show_debug(render_joints=True)

    angle_adjustment_nut = AngleAdjustmentNut(par)
    # angle_adjustment_nut.show_debug(render_joints=True)

    plate_handle_shaft = PlateHandleShaft(par)
    # plate_handle_shaft.show_debug(render_joints=True)

    plate_holder_handle = PlateHolderHandle(par)
    # plate_holder_handle.show_debug(render_joints=True)

    diamond_plate_holder = DiamondPlateHolder(par)
    # diamond_plate_holder.show_debug(render_joints=True)

    aa_screw_key = AAScrewKey(par)
    # aa_screw_key.show_debug(render_joints=True)

    washer = Washer(par)
    # washer.show_debug(render_joints=True)

    knife_example = KnifeExample(par)
    # knife_example.show_debug(render_joints=True)

    ############# ASSEMBLE JOINTS #######################
    base_plate.joints["j1"].connect_to(tower.joints["j1"])
    tower.joints["j2"].connect_to(clamp_arm_holder.joints["j1"])
    tower.joints["j3"].connect_to(angle_adjustment_screw.joints["j1"])
    tower.joints["j4"].connect_to(aa_screw_key.joints["j1"])
    angle_adjustment_screw.joints["j2"].connect_to(angle_adjustment_nut.joints["j1"])
    angle_adjustment_nut.joints["j2"].connect_to(plate_handle_shaft.joints["j1"])
    plate_handle_shaft.joints["j2"].connect_to(plate_holder_handle.joints["j1"])
    plate_holder_handle.joints["j2"].connect_to(diamond_plate_holder.joints["j1"])
    clamp_arm_holder.joints["j2"].connect_to(clamping_screw.joints["j1"])
    clamp_arm_holder.joints["j3"].connect_to(long_pin_1.joints["j1"])
    clamp_arm_holder.joints["j4"].connect_to(long_pin_2.joints["j1"])
    clamp_arm_holder.joints["j5"].connect_to(knife_example.joints["j1"])
    clamping_screw.joints["j2"].connect_to(tapered_clamping_nut.joints["j1"])
    clamping_screw.joints["j3"].connect_to(washer.joints["j1"])
    long_pin_1.joints["j2"].connect_to(clamp_arm.joints["j1"])
    long_pin_2.joints["j2"].connect_to(clamp_arm_mirror.joints["j1"])

    clamp_arm2 = clamp_arm.solid().rotate(Axis((-49.9, -60, 51.9), (1, 0, 0)), -5)
    clamp_arm3 = clamp_arm_mirror.solid().rotate(Axis((-49.9, -60, 81.9), (1, 0, 0)), 5)
    tapered_clamping_nut2 = Pos(X=30) * tapered_clamping_nut.solids()[0]
    ############# APPLY MATERIALS and SHOW ###############
    from bd_materials import metals, plastics, processes

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
    angle_adjustment_screw.material = plastics.asa(
        color="chartreuse", process=processes.fdm(mm_per_uv=0.3)
    )
    angle_adjustment_nut.material = plastics.asa(
        color="plum", process=processes.fdm(mm_per_uv=0.3)
    )
    clamp_arm.material = plastics.asa(
        color="plum", process=processes.fdm(mm_per_uv=0.3)
    )
    clamp_arm_mirror.material = plastics.asa(
        color="plum", process=processes.fdm(mm_per_uv=0.3)
    )
    long_pin_1.material = plastics.asa(
        color="chartreuse", process=processes.fdm(mm_per_uv=0.3)
    )
    long_pin_2.material = plastics.asa(
        color="chartreuse", process=processes.fdm(mm_per_uv=0.3)
    )
    tapered_clamping_nut.material = plastics.asa(
        color="salmon", process=processes.fdm(mm_per_uv=0.3)
    )
    knife_example.material = metals.stainless()

    # for solid in clamping_screw.solids():
    # solid.material = plastics.asa(color="chartreuse", process=processes.fdm(mm_per_uv=.5))
    show_all(render_joints=True)
