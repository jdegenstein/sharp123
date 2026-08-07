# %%
from build123d import *
from ocp_vscode import *

show_clear()
set_defaults(ortho=True, default_edgecolor="#121212")
# %%
from sharp123 import BuildParameters, DebugMixin

# TODO: add rectangular shaft retainer that will be used to retain angle adjustment screw


# short pin is NOT actually used in the current version

# class ShortPin(BasePartObject, DebugMixin):
#     def __init__(
#         self,
#         par: BuildParameters,
#         debug: bool = False,
#         rotation: RotationLike = Rotation(0, 0, 0),
#         align: tuple[Align, Align, Align] = (Align.CENTER, Align.CENTER, Align.CENTER),
#         mode: Mode = Mode.ADD,
#     ):
#         short_pin_len = 25
#         short_pin_d = 8

#         with BuildPart() as p_short_pin:
#             with BuildSketch() as s_short_pin:
#                 Circle(short_pin_d / 2)
#             extrude(amount=short_pin_len)
#             chamfer(edges(), par.small_parts.pin_chamfer)

#         super().__init__(
#             part=p_short_pin.part, rotation=rotation, align=align, mode=mode
#         )

#         # 2. Capture all local variables from this __init__ frame
#         self.capture_debug_locals()

#         # 3. Optionally show immediately if debug flag was passed
#         if debug:
#             self.show_debug()


class LongPin(BasePartObject, DebugMixin):
    def __init__(
        self,
        par: BuildParameters,
        debug: bool = False,
        rotation: RotationLike = Rotation(0, 0, 0),
        align: tuple[Align, Align, Align] = (Align.CENTER, Align.CENTER, Align.CENTER),
        mode: Mode = Mode.ADD,
    ):
        long_pin_len = par.tower.trap_width
        long_pin_d = (
            par.clamp_arm_holder.pin_dia
        )  # TODO: bind to parameters driven by clamp arm holder

        with BuildPart() as p_long_pin:
            with BuildSketch() as s_long_pin:
                Circle(long_pin_d / 2)  # circular or regular polygon?
            extrude(amount=long_pin_len)
            chamfer(edges(), par.small_parts.pin_chamfer)

            RigidJoint("j1", joint_location=Location())  # to clamp arm holder, LHS side
            RigidJoint(
                "j2",
                joint_location=Location((0, 0, long_pin_len / 2)),
            )  # to clamp arm midpoint

        super().__init__(
            part=p_long_pin.part, rotation=rotation, align=align, mode=mode
        )

        # 2. Capture all local variables from this __init__ frame
        self.capture_debug_locals()

        # 3. Optionally show immediately if debug flag was passed
        if debug:
            self.show_debug()


class PlateHandleShaft(BasePartObject, DebugMixin):
    def __init__(
        self,
        par: BuildParameters,
        debug: bool = False,
        rotation: RotationLike = Rotation(0, 0, 0),
        align: tuple[Align, Align, Align] = (Align.CENTER, Align.CENTER, Align.CENTER),
        mode: Mode = Mode.ADD,
    ):
        shaft_len = 250
        shaft_d = 10

        with BuildPart() as p_plate_handle_shaft:
            with BuildSketch() as s_shaft:
                RegularPolygon(shaft_d / 2, 6)
            extrude(amount=shaft_len)
            chamfer(
                edges(), par.small_parts.pin_chamfer
            )  # TODO: maybe make this end caps only
            RigidJoint("j1", joint_location=Pos(Z=20))  # to angle adjustment nut
            RigidJoint(
                "j2", joint_location=Pos(Z=shaft_len - 20)
            )  # to plate holder handle, TODO: parameterize

        super().__init__(
            part=p_plate_handle_shaft.part, rotation=rotation, align=align, mode=mode
        )

        # 2. Capture all local variables from this __init__ frame
        self.capture_debug_locals()

        # 3. Optionally show immediately if debug flag was passed
        if debug:
            self.show_debug()


class Washer(BasePartObject, DebugMixin):
    def __init__(
        self,
        par: BuildParameters,
        debug: bool = False,
        rotation: RotationLike = Rotation(0, 0, 0),
        align: tuple[Align, Align, Align] = (Align.CENTER, Align.CENTER, Align.CENTER),
        mode: Mode = Mode.ADD,
    ):
        washer_od = 25
        washer_id = 11.2  # bind to clamp screw
        washer_th = 4

        with BuildPart() as p_washer:
            with BuildSketch() as s_washer:
                Circle(washer_od / 2)
                Circle(washer_id / 2, mode=Mode.SUBTRACT)
            extrude(amount=washer_th)

            RigidJoint("j1", joint_location=Pos(Z=washer_th))  # to clamp screw end

        super().__init__(part=p_washer.part, rotation=rotation, align=align, mode=mode)

        # 2. Capture all local variables from this __init__ frame
        self.capture_debug_locals()

        # 3. Optionally show immediately if debug flag was passed
        if debug:
            self.show_debug()


class AAScrewKey(BasePartObject, DebugMixin):
    def __init__(
        self,
        par: BuildParameters,
        debug: bool = False,
        rotation: RotationLike = Rotation(0, 0, 0),
        align: tuple[Align, Align, Align] = Align.NONE,
        mode: Mode = Mode.ADD,
    ):
        with BuildPart() as p_aa_screw_key:
            with BuildSketch() as s:
                Rectangle(10 - par.clearance, 4.5 - par.clearance)
            extrude(amount=65)

            RigidJoint(
                "j1",
                joint_location=Location(),
            )

        super().__init__(
            part=p_aa_screw_key.part, rotation=rotation, align=align, mode=mode
        )

        # 2. Capture all local variables from this __init__ frame
        self.capture_debug_locals()

        # 3. Optionally show immediately if debug flag was passed
        if debug:
            self.show_debug()


if __name__ == "__main__":
    from sharp123 import create_assembly_config

    par = create_assembly_config()

    ############################
    # short pin is not used
    # short_pin = ShortPin(par)
    # short_pin.show_debug(render_joints=True)

    part_template = LongPin(par)
    part_template.show_debug(render_joints=True)

    plate_handle_shaft = PlateHandleShaft(par)
    plate_handle_shaft.show_debug(render_joints=True)

    washer = Washer(par)
    washer.show_debug(render_joints=True)

    aa_screw_key = AAScrewKey(par)
    aa_screw_key.show_debug(render_joints=True)
