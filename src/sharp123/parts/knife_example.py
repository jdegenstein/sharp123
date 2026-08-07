# %%
from build123d import *
from ocp_vscode import *

show_clear()
set_defaults(ortho=True, default_edgecolor="#121212")
# %%
from sharp123 import BuildParameters, DebugMixin


class KnifeExample(BasePartObject, DebugMixin):
    def __init__(
        self,
        par: BuildParameters,
        debug: bool = False,
        rotation: RotationLike = Rotation(0, 0, 0),
        align: tuple[Align, Align, Align] = (Align.CENTER, Align.CENTER, Align.CENTER),
        mode: Mode = Mode.ADD,
    ):
        with BuildPart() as p:
            with BuildSketch() as s:
                with BuildLine() as l:
                    m1 = Spline(
                        (0, 0),
                        (-100, -0.5),
                        (-156, -6.25 / 2),
                        (-207.5, -11.75),
                    )
                    m2 = Spline(
                        m1 @ 1,
                        (-175, -27.25),
                        (-125, -38.25),
                        (-50, -44),
                        (-1, -45),
                    )
                    m3 = Spline(
                        m2 @ 1,
                        (15, -22.5),
                        (37.5, -25),
                        (62.5, -27.5),
                        (87.5, -26.5),
                        (100, -27),
                        (113, -33),
                        (125, -27),
                        (131.5, -12.5),
                        (120, -1),
                        (100, 0.5),
                        (62.5, 0.5),
                        m1 @ 0,
                    )
                make_face()
            extrude(amount=1)
            sel = faces().sort_by(Axis.Z)[-1].edges().group_by(Axis.Y)[0]
            chamfer(sel, 0.999, 2.72)  # included angle 40 degrees
            mirror(about=Plane.XY)

        with BuildPart() as p2:  # handle
            with BuildSketch(Plane.XY.offset(1)) as s2:  # handle
                add(s.sketch)
                split(bisect_by=Plane.YZ.offset(5))
            extrude(amount=10)

            sel = faces().sort_by(Axis.Z)[-1].edges().sort_by(Axis.X)[0]
            chamfer(sel, 8.99)
            sel = faces().sort_by(Axis.Z)[-1].edges().filter_by(GeomType.BSPLINE)
            fillet(sel, 6)
            mirror(about=Plane.XY)

        comp = Compound([p.part, p2.part])

        RigidJoint(  # to clamp arm holder
            "j1",
            to_part=comp,
            joint_location=Location(Plane((0, 0, 0), x_dir=(-1, 0, 0))),
        )

        super().__init__(part=comp, rotation=rotation, align=align, mode=mode)

        # 2. Capture all local variables from this __init__ frame
        self.capture_debug_locals()

        # 3. Optionally show immediately if debug flag was passed
        if debug:
            self.show_debug()


if __name__ == "__main__":
    from sharp123 import create_assembly_config

    par = create_assembly_config()
    knife_example = KnifeExample(par)
    knife_example.show_debug(render_joints=True)
