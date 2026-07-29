from build123d import *
from build123d.build_common import validate_inputs, WorkplaneList
from enum import Enum, auto
import math
import copy

# Only makes sense if/when you know which direction you're looking the plane from (ie. when you have a workplane?)
class TangentDirection(Enum):
    """Direction of tangent [on a circle]"""
    LEAVE_CW = auto()
    LEAVE_CCW = auto()
    ENTER_CW = LEAVE_CCW
    ENTER_CCW = LEAVE_CW

    # When there's a source/target circle, these kind of make sense (in relation to a line from source to target)
    LEAVE_LEFT = LEAVE_CW
    LEAVE_RIGHT = LEAVE_CCW
    ENTER_LEFT = ENTER_CW
    ENTER_RIGHT = ENTER_CCW

    SRC_LEFT = LEAVE_CW
    SRC_RIGHT = LEAVE_CCW
    DST_LEFT = ENTER_CW
    DST_RIGHT = ENTER_CCW

class DoubleCircleTangentLine(BaseLineObject):
    """Line Object: Line tangent to two circles

    Create a straight line, tangent to two circles.

    If there is no active workplane, the tangent direction is essentially random.

    Args:
        mode (Mode, optional): combination mode. Defaults to Mode.ADD.

    Raises:
        ValueError: Two point not provided
    """

    _applies_to = [BuildLine._tag]

    def __init__(
        self,
        src_center: VectorLike,
        src_radius: float,
        src_dir: TangentDirection,
        dst_center: VectorLike,
        dst_radius: float,
        dst_dir: TangentDirection,
        mode: Mode = Mode.ADD
    ):

        context: BuildLine = BuildLine._get_context(self)
        validate_inputs(context, self)

        if WorkplaneList._get_context() is not None:
            workplane = WorkplaneList._get_context().workplanes[0]
            src_center, dst_center = [workplane.to_local_coords(pt) if isinstance(pt, Vector) else Vector(pt) for pt in (src_center, dst_center)]
        else:
            raise NotImplementedError("DoubleCircleTangentLine is only implemented with an active workplane")

        assert src_center.Z == 0 and dst_center.Z == 0

        # Radius of the construction circle is:
        # - difference of the radii, for outer tangents
        # - sum of the radii, for inner tangents
        rsign = (1, -1)[src_dir != dst_dir]
        r = src_radius + rsign * dst_radius
        sign = 1 if r >= 0 else -1

        v = dst_center - src_center
        d = v.length

        asign = {TangentDirection.LEAVE_CW: 1, TangentDirection.LEAVE_CCW: -1}[src_dir]
        a = asign * math.degrees(math.acos(r/d))
        t = v.rotate(Axis.Z, a).normalized()
        p = -rsign * dst_radius * t

        t0, t1 = src_center + t*r + p, dst_center + p

        pts = WorkplaneList.localize(t0.to_tuple(), t1.to_tuple())

        p0, p1 = [Vector(p) for p in pts]

        new_edge = Edge.make_line(p0, p1)
        super().__init__(new_edge, mode=mode)

class DoubleCircleTangentArc(BaseLineObject):
    """Line Object: Arc tangent to given tangent and circle

    Create an arc defined by a point/tangent pair and a point/radius pair to which
    the other end is tangent to.

    Contains a solver.

    Args:
        pnt (VectorLike): starting point of tangent arc
        tangent (VectorLike): tangent at starting point of tangent arc
        center (VectorLike): center point of circle
        radius (float): radius of circle
        dir (TangentDirection): which tangent of the circle to use
        mode (Mode, optional): combination mode. Defaults to Mode.ADD.

    Raises:
        RunTimeError: no double tangent arcs found
    """

    _applies_to = [BuildLine._tag]

    def __init__(
        self,
        start: VectorLike,
        tangent: VectorLike,
        center: VectorLike,
        radius: float,
        dir: TangentDirection,
        mode: Mode = Mode.ADD,
    ):
        context: BuildLine = BuildLine._get_context(self)
        validate_inputs(context, self)

        if WorkplaneList._get_context() is not None:
            workplane = WorkplaneList._get_context().workplanes[0]
            start, tangent, center = [workplane.to_local_coords(pt) if isinstance(pt, Vector) else Vector(pt) for pt in (start, tangent, center)]
            #start, tangent, center = map(Vector, (start, tangent, center))
        else:
            raise NotImplementedError("DoubleCircleTangentArc is only implemented with an active workplane")

        assert start.Z == 0 and tangent.Z == 0 and center.Z == 0

        sign = {TangentDirection.LEAVE_CW: 1, TangentDirection.LEAVE_CCW: -1}[dir]

        p = tangent.rotate(Axis.Z, -90)
        v = center - start
        c = v.rotate(Axis.Z, -tangent.get_signed_angle(Axis.Y.direction))
        d = (c.Y**2 + c.X**2 - radius**2) / (2 * (c.X + sign*radius))
        arc_center = start + p.normalized() * d

        #assert False, (start, center, arc_center, '|', c, radius, d)
        #start, center, arc_center = WorkplaneList.localize(start.to_tuple(), center.to_tuple(), arc_center.to_tuple())

        # Could also calculate the tangent point by end = arc_center + (center - arc_center).normalized() * d
        #arc = Edge.make_tangent_arc(
        #     start, tangent, end
        #)

        arc = Edge.make_circle(
            d,
            workplane.shift_origin(arc_center),
            start_angle=(start - arc_center).get_signed_angle(Axis.X.direction),
            end_angle=(center - arc_center).get_signed_angle(Axis.X.direction),
            angular_direction=AngularDirection.CLOCKWISE if d != 0 else AngularDirection.COUNTER_CLOCKWISE,
        )

        super().__init__(arc, mode=mode)

def centerarc_from_endpoints(center, radius, start, end, direction):
    start_vec = start - center
    end_vec = end - center
    start_angle = start_vec.get_signed_angle(Axis.X.direction)
    arc_size = end_vec.get_signed_angle(start_vec) % 360

    if direction == AngularDirection.CLOCKWISE:
        arc_size -= 360

    CenterArc(center, radius, start_angle, arc_size)

with BuildPart() as part:
    with BuildSketch():
        with BuildLine() as l:
            c = (-0.982, 0.744)
            ct, cm, cb = (-0.625, 5.85), (-0.66, 5.3), (0, 1.65)
            rt, rm, rb = 0.1, 0.4, 0.5
            # Failed to find a solution
            #t = CenterArc(ct, rt, 0, 360)
            #DoubleTangentArc(c, Axis.Y.direction, t, keep=Keep.TOP)
            l0 = DoubleCircleTangentArc(
                c, Axis.Y.direction,
                ct, rt, TangentDirection.DST_LEFT,
            )
            l1 = DoubleCircleTangentLine(
                ct, rt, TangentDirection.SRC_LEFT,
                cm, rm, TangentDirection.DST_LEFT,
            )
            l2 = DoubleCircleTangentLine(
                cm, rm, TangentDirection.SRC_LEFT,
                cb, rb, TangentDirection.DST_RIGHT,
            )
            centerarc_from_endpoints(ct, rt, l0 @ 1, l1 @ 0, AngularDirection.CLOCKWISE)
            centerarc_from_endpoints(cm, rm, l1 @ 1, l2 @ 0, AngularDirection.CLOCKWISE)
            centerarc_from_endpoints(cb, rb, l2 @ 1, -Axis.Y.direction, AngularDirection.COUNTER_CLOCKWISE)
            Line(c, (0, c[1]))
            mirror(about=Plane.YZ)
        make_face()
    extrude(amount=0.1)

#show_object(l)
#show_object(part)

