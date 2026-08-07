# %%
from build123d import *
from ocp_vscode import *

show_clear()
set_defaults(ortho=True, default_edgecolor="#121212")
# %%
from bd_warehouse import thread
from sharp123 import BuildParameters, DebugMixin


class AngleAdjustmentNut(BasePartObject, DebugMixin):
    def __init__(
        self,
        par: BuildParameters,
        debug: bool = False,
        rotation: RotationLike = Rotation(0, 0, 0),
        align: tuple[Align, Align, Align] = Align.NONE,
        mode: Mode = Mode.ADD,
    ):
        with BuildPart() as p_angle_adjustment_nut:
            with BuildSketch() as s:
                with Locations((0, 10)):
                    Trapezoid(40, 27.5, 65, align=(Align.CENTER, Align.MAX))
                Circle(14 / 2, mode=Mode.SUBTRACT)
            extrude(amount=18)
            with BuildSketch(faces().sort_by(Axis.Y)[-1]) as s:
                Rectangle(5, 18)
            extrude(amount=18)
            holef = faces().filter_by(Axis.X).sort_by(Axis.X)[-1]
            with Locations(holef):
                Hole(10 / 2)
            newe = edges(Select.NEW)
            chamfer(newe, 2.4)

            sel = faces().sort_by(Axis.Y)[-1].edges().filter_by(Axis.X)
            chamfer(sel, 3)

            sel2 = (
                faces().filter_by(Axis.Y).group_by(Axis.Y)[-2].edges().filter_by(Axis.Z)
            )
            fillet(sel2, 1)

        mtt = thread.MetricTrapezoidalThread("14x3", 18, external=False)
        assy_angle_nut = Compound([p_angle_adjustment_nut.part, *mtt.solids()])

        RigidJoint(  # to angle adjustment screw
            "j1",
            to_part=assy_angle_nut,
            joint_location=Pos(Z=15 / 2),
        )

        RigidJoint(  # to handle shaft, TODO: improve positioning
            "j2",
            to_part=assy_angle_nut,
            joint_location=Location(Plane(newe[0].arc_center, z_dir=(1, 0, 0))),
        )

        super().__init__(part=assy_angle_nut, rotation=rotation, align=align, mode=mode)

        # 2. Capture all local variables from this __init__ frame
        self.capture_debug_locals()

        # 3. Optionally show immediately if debug flag was passed
        if debug:
            self.show_debug()


if __name__ == "__main__":
    from sharp123 import create_assembly_config

    par = create_assembly_config()
    angle_adjustment_nut = AngleAdjustmentNut(par)
    angle_adjustment_nut.show_debug(render_joints=True)
