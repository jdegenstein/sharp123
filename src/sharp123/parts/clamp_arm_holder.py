# %%
from build123d import *
from ocp_vscode import *

show_clear()
set_defaults(ortho=True, default_edgecolor="#121212")
# %%
from sharp123 import BuildParameters, DebugMixin

# TODO: add parameterization, add splits and alignment pin holes, cross check dimensions against other parts


class ClampArmHolder(BasePartObject, DebugMixin):
    def __init__(
        self,
        par: BuildParameters,
        debug: bool = False,
        rotation: RotationLike = Rotation(0, 0, 0),
        align: tuple[Align, Align, Align] = Align.NONE,
        mode: Mode = Mode.ADD,
    ):
        with BuildPart() as p_clamp_arm_holder:
            with BuildSketch() as s:
                Rectangle(100, par.tower.trap_width, align=(Align.MIN, Align.CENTER))
                with Locations((10, 0)):
                    Rectangle(
                        100,
                        par.tower.trap_width - 20,
                        align=(Align.MIN, Align.CENTER),
                        mode=Mode.SUBTRACT,
                    )
            extrude(amount=par.clamp_arm_holder.octagon_dia / 2, both=True)
            # TODO^ clamp arm holder is wider than octagon which is ok but not clear from this

            with BuildSketch(Plane.YZ.offset(0)) as s2:
                RegularPolygon(
                    par.clamp_arm_holder.octagon_dia / 2,
                    8,
                    rotation=360 / 8 / 2,
                )
            extrude(amount=-par.base_plate.cutout_len)

            edgs = faces().group_by(Axis.X)[-1].edges().filter_by(Axis.Y)
            chamfer(edgs, 40, 15)

            sel0 = (
                faces()
                .sort_by(Axis.Y)[-1]
                .edges()
                .filter_by(Axis.Z)
                .sort_by(Axis.X)[-1]
            )
            pln = Plane(sel0 @ 0.5, (1, 0, 0), (0, 1, 0))
            with BuildSketch(pln) as s3:
                Rectangle(18 / 1.414, 18 / 1.414, rotation=45)
            extrude(amount=-100, mode=Mode.SUBTRACT)
            with Locations(Plane.XZ.offset(0)):
                with Locations((60, 15), (60, -15)):
                    Hole(8 / 2)
                with Locations((31, 0)):
                    Hole(11.5 / 2)
            sel = faces().sort_by(Axis.X)[0].center()
            RigidJoint(  # to main tower
                label="j1",
                joint_location=Location(Plane(sel, (0, -1, 0), (1, 0, 0))),
            )

            sel2 = (
                faces()
                .sort_by(Axis.Y)[0]
                .inner_wires()
                .edges()
                .sort_by(SortBy.RADIUS)[-1]
            )
            sel2c = sel2.arc_center
            RigidJoint(  # to clamping screw
                label="j2",
                joint_location=Location(Plane(sel2c, (1, 0, 0), (0, 1, 0))),
            )

            sel3 = (
                faces()
                .sort_by(Axis.Y)[0]
                .inner_wires()
                .edges()
                .group_by(SortBy.RADIUS)[0]
            )
            RigidJoint(  # to clamp arm pin (long pin) -- bottom
                label="j3",
                joint_location=Location(
                    Plane(sel3.sort_by(Axis.Z)[0].arc_center, (1, 0, 0), (0, 1, 0))
                ),
            )
            RigidJoint(  # to second clamp arm pin (long pin) -- top
                label="j4",
                joint_location=Location(
                    Plane(sel3.sort_by(Axis.Z)[-1].arc_center, (1, 0, 0), (0, 1, 0))
                ),
            )
            RigidJoint(  # to example knife
                label="j5",
                joint_location=Location(Plane((90.999, 49.9, 0), (1, 0, 0), (0, 0, 1))),
            )

        super().__init__(
            part=p_clamp_arm_holder.part, rotation=rotation, align=align, mode=mode
        )

        # 2. Capture all local variables from this __init__ frame
        self.capture_debug_locals()

        # 3. Optionally show immediately if debug flag was passed
        if debug:
            self.show_debug()


if __name__ == "__main__":
    from sharp123 import create_assembly_config

    par = create_assembly_config()
    clamp_arm_holder = ClampArmHolder(par)
    clamp_arm_holder.show_debug(render_joints=True)
