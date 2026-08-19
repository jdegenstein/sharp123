# %%
from build123d import *
from ocp_vscode import *

show_clear()
set_defaults(ortho=True, default_edgecolor="#121212")
# %%
from sharp123 import BuildParameters, DebugMixin


class ClampArm(BasePartObject, DebugMixin):
    def __init__(
        self,
        par: BuildParameters,
        debug: bool = False,
        rotation: RotationLike = Rotation(0, 0, 0),
        align: tuple[Align, Align, Align] = (Align.CENTER, Align.CENTER, Align.CENTER),
        mode: Mode = Mode.ADD,
    ):

        overall_height = par.clamp_arm_holder.interior_width - 1
        with BuildPart() as p_clamp_arm:
            with BuildSketch() as s:
                with BuildLine() as l:
                    m1 = FilletPolyline(
                        (0, 0),
                        (110 * 2 / 3, 0),
                        (110, -49.8 / 2 + 5),
                        (110 / 3, -49.8 / 2 + 8),
                        (110 / 3 - 10, -10),
                        (0, -10),
                        radius=[
                            90,
                            1,
                            10,
                            10,
                        ],
                    )
                    m2 = Line(m1 @ 1, m1 @ 0)
                make_face()
            extrude(amount=overall_height)

            with BuildSketch(Plane.YZ) as s2:
                with BuildLine() as l2:
                    n1 = PolarLine(
                        (-10, 0),
                        overall_height,
                        90 + 5,
                        length_mode=LengthMode.VERTICAL,
                    )
                    n2 = PolarLine(n1 @ 1, -(n1 @ 1).X, 0)
                    n3 = Polyline(n2 @ 1, (0, 0), (n1 @ 0))
                make_face()
            extrude(amount=8)

            hole_loc = Location((48, -10, (overall_height) / 2))
            with Locations(hole_loc):
                Hole(par.clamp_arm_holder.pin_dia_hole/2)

            RigidJoint(
                "j1",
                joint_location=hole_loc,
            )

        super().__init__(
            part=p_clamp_arm.part, rotation=rotation, align=align, mode=mode
        )

        # 2. Capture all local variables from this __init__ frame
        self.capture_debug_locals()

        # 3. Optionally show immediately if debug flag was passed
        if debug:
            self.show_debug()


if __name__ == "__main__":
    from sharp123 import create_assembly_config

    par = create_assembly_config()
    clamp_arm = ClampArm(par)
    clamp_arm.show_debug(render_joints=True)
