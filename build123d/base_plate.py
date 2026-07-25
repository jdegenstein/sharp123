# %%
from build123d import *
from ocp_vscode import *

show_clear()
set_defaults(ortho=True, default_edgecolor="#121212")
# %%


with BuildPart() as p_base_plate:
    with BuildSketch() as s:
        RectangleRounded(125, 150, 10)
    extrude(amount=20 / 2, both=True)

    edgs = faces().sort_by(Axis.Z)[-1].edges().group_by(Axis.Y)[0:3]

    with BuildSketch(Plane.XZ.offset(0)) as s:
        Trapezoid(100, 10, 45, align=(Align.CENTER, Align.MIN))
    extrude(amount=-100, mode=Mode.SUBTRACT)

    chamfer(edgs, 8)

    # with BuildSketch(Plane.XY.offset(20 / 2)) as s:
    #     with Locations((0, -50)):
    #         Text("sharp123", 15)
    # extrude(amount=-3, mode=Mode.SUBTRACT)


set_colormap(ColorMap.golden_ratio())
# fmt: off
show_all(
    classes = [BuildPart, BuildSketch, BuildLine, ],  # comment to show all objects
    include = ["", ],
    exclude = ["", ],
    show_locals = False,
    helper_scale = 1,  # controls size of e.g. planes and axes
)  # fmt: on
