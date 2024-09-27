# %%
from build123d import *
from ocp_vscode import *
from inspect import currentframe as cf
from tangentline import *

set_port(3939)
show_clear()
set_defaults(ortho=True, default_edgecolor="#121212", reset_camera=Camera.KEEP)
# %%

clamp_th = 16
hole_r = 5 / 2
hole_pos = (0,0)
hole_wall = 2
hole_r_out = hole_r + hole_wall
front_len = 30
back_len = 30
back_thick = hole_r_out

tip_r = 1 / 2
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
  
def clamp_shape(thick_offset=0):
  back_thick2 = back_thick + thick_offset
  back = [
    (0,hole_r_out),
    (back_len, hole_r_out),
    (back_len, hole_r_out - back_thick2),
    (back_len - 5, hole_r_out - back_thick2),
    (back_len - 5, hole_r_out - back_thick + 0.1 ),
    (hole_r_out + 5, hole_r_out - back_thick),
  ]  
  with BuildSketch() as s_clamp:
    with BuildLine() as l_clamp:
      l0 = DoubleCircleTangentLine(
          hole_pos, hole_r_out, TangentDirection.SRC_LEFT,
          tip_pos, tip_r, TangentDirection.DST_LEFT,
      )
      l1 = DoubleCircleTangentLine(
          hole_pos, hole_r_out, TangentDirection.SRC_RIGHT,
          tip_pos, tip_r, TangentDirection.DST_RIGHT,
      )
      centerarc_from_endpoints(tip_pos, tip_r, l0 @ 1, l1 @ 1, AngularDirection.CLOCKWISE)
      RadiusArc(l1 @ 0, back[0], hole_r_out)
      Polyline(back)
      # FilletPolyline(back, radius=1)
      a0 = CenterArc(hole_pos, hole_r_out, 270, 60)
      TangentArc([back[-1], a0 @1], tangent=(-1,0))
    make_face()
    # Circle(hole_r, mode=Mode.SUBTRACT)
  return s_clamp.sketch

with BuildPart() as p_clamp:
    with BuildSketch(Plane.XY) as s_clamp1:
        add(clamp_shape(0))
    with BuildSketch(Plane.XY.offset(clamp_th)) as s_clamp2:
        add(clamp_shape(3))
    loft()
    with BuildSketch() as s:
        Circle(hole_r)
    extrude(amount=clamp_th, mode=Mode.SUBTRACT)

show([
   p_clamp, 
  # s_clamp1,
   *helpers,
])
# %%
