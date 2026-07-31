# %%
from build123d import *
from ocp_vscode import *

set_defaults(ortho=True, default_edgecolor="#121212")
# %%

from bd_warehouse import thread
from sharp123 import BuildParameters, DebugMixin


# TODO: parameterize and check against other parts
class ClampingScrew(BasePartObject, DebugMixin):
    def __init__(
        self,
        par: BuildParameters,
        debug: bool = False,
        rotation: RotationLike = Rotation(0, 0, 0),
        align: tuple[Align, Align, Align] = (Align.CENTER, Align.CENTER, Align.CENTER),
        mode: Mode = Mode.ADD,
    ):
        mtt_extern = thread.MetricTrapezoidalThread(
            "14x3", par.tower.trap_width, external=True
        )
        with BuildPart() as p_angle_screw:
            with BuildSketch() as s:
                Circle(11 / 2)
            extrude(amount=par.tower.trap_width)
            with BuildSketch() as s2:
                Circle(14 / 2)
            extrude(amount=-7)
            with BuildSketch(faces().sort_by(Axis.Z)[-1]) as s3:
                Circle(9 / 2)
            extrude(amount=7)
            topfe = faces().sort_by(Axis.Z)[-1].edges()
            chamfer(topfe, 1)
            with BuildSketch(faces().sort_by(Axis.Z)[0]) as s4:
                Circle(20 / 2)
            extrude(amount=3)
            botf0 = faces().sort_by(Axis.Z)[0].edges()
            with BuildSketch(faces().sort_by(Axis.Z)[0]) as s_knob:
                RegularPolygon(40 / 2, 6)
                with Locations((vertices())):
                    Circle(5, mode=Mode.SUBTRACT)
                fillet(vertices(), 1)
            extrude(amount=15)
            botf = faces().sort_by(Axis.Z)[0].edges()
            midf = faces().filter_by(Axis.Z).sort_by(Axis.Z)[1].outer_wire().edges()
            chamfer(botf, 1)
            chamfer(midf, 0.99)
            fillet(botf0, 2.5)

            sel = faces().filter_by(Axis.Z).sort_by(Axis.Z)[2].center()

        assy_angle_screw = Compound([p_angle_screw.part, *mtt_extern.solids()])
        # TODO^ figure out why I need to use mtt_extern.solids() -- seems like a bug upstream
        RigidJoint(  # to clamp arm holder
            label="j1",
            to_part=assy_angle_screw,
            joint_location=Location(Plane(sel, (1, 0, 0), (0, 0, 1))),
        )

        RigidJoint(  # to tapered clamping nut
            label="j2",
            to_part=assy_angle_screw,
            joint_location=Location(Plane((0, 0, 0), (1, 0, 0), (0, 0, 1))),
        )

        super().__init__(
            part=assy_angle_screw, rotation=rotation, align=align, mode=mode
        )

        # 2. Capture all local variables from this __init__ frame
        self.capture_debug_locals()

        # 3. Optionally show immediately if debug flag was passed
        if debug:
            self.show_debug()


if __name__ == "__main__":
    from sharp123 import create_assembly_config

    par = create_assembly_config()
    clamping_screw = ClampingScrew(par)
    clamping_screw.show_debug(render_joints=True)
