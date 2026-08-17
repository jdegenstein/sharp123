# %%
from build123d import *
from ocp_vscode import *

show_clear()
set_defaults(ortho=True, default_edgecolor="#121212")
# %%
from bd_warehouse import thread
from sharp123 import BuildParameters, DebugMixin, PrintableMetricTrapezoidalThread


# TODO: check parameterization against other parts, especially taper angle
class TaperedClampingNut(BasePartObject, DebugMixin):
    def __init__(
        self,
        par: BuildParameters,
        debug: bool = False,
        rotation: RotationLike = Rotation(0, 0, 0),
        align: tuple[Align, Align, Align] = (Align.CENTER, Align.CENTER, Align.CENTER),
        mode: Mode = Mode.ADD,
    ):
        with BuildPart() as p_tapered_clamping_nut:
            with BuildSketch() as s:
                SlotCenterPoint((0, 0), (10, 0), 18)
            extrude(amount=20)
            split(bisect_by=Plane.YZ)

            with BuildSketch(Plane.YZ) as s2:
                Trapezoid(33, 20, 85, align=(Align.CENTER, Align.MIN))
            extrude(amount=-9)

            hole_loc = Location((10, 0))
            with Locations(hole_loc):
                Hole(14.6 / 2)

        mtt = PrintableMetricTrapezoidalThread("14x3", 20, external=False, clearance=0.7)
        mtt = Pos(10, 0) * mtt

        # explode solids into compound to work around possible joint bug in bd_warehouse or build123d
        assy_tapered_clamping_nut = Compound(
            [
                p_tapered_clamping_nut.part,
                *mtt.solids(),
            ]
        )

        RigidJoint(  # to clamp arm holder
            label="j1",
            to_part=assy_tapered_clamping_nut,
            joint_location=Location(hole_loc),
        )

        super().__init__(
            part=assy_tapered_clamping_nut, rotation=rotation, align=align, mode=mode
        )

        # 2. Capture all local variables from this __init__ frame
        self.capture_debug_locals()

        # 3. Optionally show immediately if debug flag was passed
        if debug:
            self.show_debug()


if __name__ == "__main__":
    from sharp123 import create_assembly_config

    par = create_assembly_config()
    tapered_clamping_nut = TaperedClampingNut(par)
    tapered_clamping_nut.show_debug(render_joints=True)
