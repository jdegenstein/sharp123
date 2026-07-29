# %%
from build123d import *
from ocp_vscode import *

show_clear()
set_defaults(ortho=True, default_edgecolor="#121212")
# %%
from sharp123 import BuildParameters, DebugMixin

# TODO: parameterize and check against other parts
class BasePlate(BasePartObject, DebugMixin):
    def __init__(
        self,
        par: BuildParameters,
        debug: bool= False,
        rotation: RotationLike = Rotation(0,0,0),
        align: tuple[Align, Align, Align] = (Align.CENTER, Align.CENTER, Align.CENTER),
        mode: Mode = Mode.ADD,
    ):
        with BuildPart() as p_base_plate:
            with BuildSketch() as s:
                RectangleRounded(125, 150, 10)
            extrude(amount=20 / 2, both=True)

            edgs = faces().sort_by(Axis.Z)[-1].edges().group_by(Axis.Y)[0:3]

            with BuildSketch(Plane.XZ.offset(0)) as s:
                Trapezoid(100, 10, 45, align=(Align.CENTER, Align.MIN))
            extrude(amount=-100, mode=Mode.SUBTRACT)

            chamfer(edgs, 8)

            sel = faces().filter_by(Axis.Y).sort_by(Axis.Y)[1].edges().sort_by(Axis.Z)[0]

            with BuildSketch(Plane.XY.offset(20 / 2)) as s:
                with Locations((0, -50)):
                    Text("sharp123", 15)
            extrude(amount=-3, mode=Mode.SUBTRACT)

            RigidJoint(
                label="j1",
                joint_location=Location(Plane(sel@.5,(1,0,0),(0,-1,0)))
            )

        super().__init__(part=p_base_plate.part, rotation=rotation, align=align, mode=mode)

        # 2. Capture all local variables from this __init__ frame
        self.capture_debug_locals()

        # 3. Optionally show immediately if debug flag was passed
        if debug:
            self.show_debug()


set_colormap(ColorMap.golden_ratio())
# fmt: off
show_all(
    classes = [BuildPart, BuildSketch, BuildLine, ],  # comment to show all objects
    include = ["sel", ],
    exclude = ["", ],
    show_locals = False,
    helper_scale = 1,  # controls size of e.g. planes and axes
)  # fmt: on
