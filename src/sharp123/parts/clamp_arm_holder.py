# %%
from build123d import *
from ocp_vscode import *
from inspect import currentframe as cf

set_port(3939)
show_clear()
set_defaults(ortho=True, default_edgecolor="#121212")
# %%

# TODO: add parameterization, add splits and alignment pin holes, cross check dimensions against other parts

with BuildPart() as p_clamp_arm_holder:
    with BuildSketch() as s:
        Rectangle(100, 80, align=(Align.MIN, Align.CENTER))
        with Locations((10, 0)):
            Rectangle(100, 80 - 20, align=(Align.MIN, Align.CENTER), mode=Mode.SUBTRACT)
    extrude(amount=40 / 2, both=True)

    with BuildSketch(Plane.YZ.offset(0)) as s:
        RegularPolygon(20, 8, rotation=360 / 8 / 2, major_radius=False)
    extrude(amount=-60)

    edgs = faces().group_by(Axis.X)[-1].edges().filter_by(Axis.Y)
    chamfer(edgs, 40, 10)

    with Locations(Plane.XZ.offset(0)):
        with Locations((60, 10), (60, -10)):
            Hole(8 / 2)
        with Locations((35, 0)):
            Hole(15 / 2)


set_colormap(ColorMap.golden_ratio())
# fmt: off
show_all(
    classes = [BuildPart, BuildSketch, BuildLine, ],  # comment to show all objects
    include = ["", ],
    exclude = ["", ],
    show_locals = False,
    helper_scale = 1,  # controls size of e.g. planes and axes
)  # fmt: on
