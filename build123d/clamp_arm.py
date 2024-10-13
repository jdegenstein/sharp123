# %%
from build123d import *
from ocp_vscode import *
from inspect import currentframe as cf
from tangentline import *

set_port(3939)
show_clear()
set_defaults(ortho=True, default_edgecolor="#121212", reset_camera=Camera.KEEP, render_joints=True)
import importlib
import project_dimensions

# %%

importlib.reload(project_dimensions)
clamp_arm = project_dimensions.project_dimensions.clamp_arm
internal_width = clamp_arm.internal_width
print(internal_width) # changes with save of project_dimensions.py

clamp_th = internal_width
hole_r = 8 / 2
hole_pos = (0, 0)
hole_wall = 3
hole_r_out = hole_r + hole_wall
front_len = 50
back_len = 50
back_thick = hole_r_out
back_ridge_width = 8

tip_r = 3 / 2
# tip is defined as a circle
# edge of the tip is front_len from origin (not the center of it)
tip_pos = (-front_len + tip_r, tip_r - hole_r_out)


with BuildSketch() as s_helpers:
    with Locations(tip_pos):
        Circle(tip_r)

hole_out = Circle(hole_r_out)
helpers = [
    Circle(hole_r),
    hole_out,
    s_helpers,
]


def clamp_shape(back_ridge_height=0):
    back_thick2 = back_thick + back_ridge_height
    back = [
        (0, hole_r_out),
        (back_len, hole_r_out),
        (back_len, hole_r_out - back_thick2),
        (back_len - back_ridge_width, hole_r_out - back_thick2),
        (back_len - back_ridge_width, hole_r_out - back_thick + 0.1),
        (hole_r_out + 5, hole_r_out - back_thick),
    ]
    global l_clamp
    with BuildSketch() as s_clamp:
        with BuildLine() as l_clamp:
            global l1
            global l0
            l0 = DoubleCircleTangentLine(
                hole_pos,
                hole_r_out,
                TangentDirection.SRC_LEFT,
                tip_pos,
                tip_r,
                TangentDirection.DST_LEFT,
            )
            l1 = DoubleCircleTangentLine(
                hole_pos,
                hole_r_out,
                TangentDirection.SRC_RIGHT,
                tip_pos,
                tip_r,
                TangentDirection.DST_RIGHT,
            )
            centerarc_from_endpoints(
                tip_pos, tip_r, l0 @ 1, l1 @ 1, AngularDirection.CLOCKWISE
            )
            RadiusArc(l1 @ 0, back[0], hole_r_out)
            poly = Polyline(back)
            # FilletPolyline(back, radius=1)
            a0 = CenterArc(hole_pos, hole_r_out, 270, 60)
            # TangentArc([poly@1, a0@1], tangent=a0%1, tangent_from_first=False)
            spl = Spline([poly @ 1, a0 @ 1], tangents=(poly % 1, -(a0 % 1)))
        make_face()
        # Circle(hole_r, mode=Mode.SUBTRACT)
    return s_clamp.sketch


with BuildPart() as p_clamp:
    with BuildSketch(Plane.XY) as s_clamp1:
        add(clamp_shape(0))
    with BuildSketch(Plane.XY.offset(clamp_th)) as s_clamp2:
        add(clamp_shape(8))
    loft()
    with BuildSketch() as s:
        Circle(hole_r)
    extrude(amount=clamp_th, mode=Mode.SUBTRACT)

with Locations(Plane.XY):
    locs = GridLocations(1, 1, 1, 1)
    for l in locs:
        print(l)

RigidJoint('left',to_part=p_clamp, joint_location=hole_out.location)

show(
    [
        p_clamp,
    #   p_clamp.joints['left'],
#        s_clamp1,
#        *helpers,
    ]
)

# %%
