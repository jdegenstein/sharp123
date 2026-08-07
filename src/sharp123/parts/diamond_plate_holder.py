# %%
from build123d import *
from ocp_vscode import *

show_clear()
set_defaults(ortho=True, default_edgecolor="#121212")
# %%
from sharp123 import BuildParameters, DebugMixin


class DiamondPlateHolder(BasePartObject, DebugMixin):
    def __init__(
        self,
        par: BuildParameters,
        debug: bool = False,
        rotation: RotationLike = Rotation(0, 0, 0),
        align: tuple[Align, Align, Align] = (Align.CENTER, Align.CENTER, Align.CENTER),
        mode: Mode = Mode.ADD,
    ):
        # Diamond Plate Product Dimensions	3.25"L x 2.0"W x 1/16"H
        plate_len = 3.25 * IN + 0.4
        plate_wid = 2.0 * IN + 0.4
        plate_th = 1 / 16 * IN * 0.8

        holder_th = 3

        with BuildPart() as p_diamond_plate_holder:
            with BuildSketch() as s:
                Rectangle(plate_len, plate_wid)
                offset(amount=2)
            extrude(amount=holder_th)
            with BuildSketch(faces().sort_by(Axis.Z)[-1]) as s:
                Rectangle(plate_len, plate_wid)
            extrude(amount=-plate_th, mode=Mode.SUBTRACT)

            with Locations((0, -15)):
                Hole(16 / 2)

            with Locations(Plane.XY.offset(3 - plate_th)):
                with GridLocations(plate_len * 0.8, 1, 2, 1):
                    CounterBoreHole(5 / 2, 10.5 / 2, 1)

            RigidJoint(  # to plate holder handle
                "j1",
                joint_location=Location(
                    Plane((0, 0, 0), x_dir=(0, 1, 0), z_dir=(0, 0, 1))
                ),
            )

        super().__init__(
            part=p_diamond_plate_holder.part, rotation=rotation, align=align, mode=mode
        )

        # 2. Capture all local variables from this __init__ frame
        self.capture_debug_locals()

        # 3. Optionally show immediately if debug flag was passed
        if debug:
            self.show_debug()


if __name__ == "__main__":
    from sharp123 import create_assembly_config

    par = create_assembly_config()
    diamond_plate_holder = DiamondPlateHolder(par)
    diamond_plate_holder.show_debug(render_joints=True)
