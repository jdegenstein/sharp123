# %%
from build123d import *
from ocp_vscode import *

show_clear()
set_defaults(ortho=True, default_edgecolor="#121212")
# %%
from sharp123 import BuildParameters, DebugMixin


class PlateHolderHandle(BasePartObject, DebugMixin):
    def __init__(
        self,
        par: BuildParameters,
        debug: bool = False,
        rotation: RotationLike = Rotation(0, 0, 0),
        align: tuple[Align, Align, Align] = Align.NONE,
        mode: Mode = Mode.ADD,
    ):
        with BuildPart() as p_plate_holder_handle:
            with BuildSketch(Plane.XZ.offset(0)) as s:
                Trapezoid(18, 30, 85, align=(Align.CENTER, Align.MIN))
                split(bisect_by=Plane.YZ)
                with Locations((8, 22)):
                    Circle(4, mode=Mode.SUBTRACT)
                with Locations((10, 14)):
                    Circle(6, mode=Mode.SUBTRACT)
                vtxs = vertices().sort_by(Axis.X)[-5:-1]
                fillet(vtxs, 2)
            extrude(amount=3 * 25 / 2, both=True)

            with BuildSketch(Plane.YZ.offset(0)) as s2:
                Trapezoid(3 * 25, 30, 80, align=(Align.CENTER, Align.MIN))
                vtxs2 = vertices().group_by(Axis.Y)[-1]
                fillet(vtxs2, 12)
            extrude(amount=14, both=True, mode=Mode.INTERSECT)
            # newe = edges(Select.NEW).group_by(Axis.X)[1::] # TODO: fix fillet
            # fillet(newe, 0.01)
            mirror(about=Plane.YZ)

            with BuildSketch(Plane.XZ.offset(0)) as s3:
                with Locations((0, 6)):
                    RegularPolygon(10.3 / 2, 6)
            extrude(amount=100, mode=Mode.SUBTRACT)

            newe2 = edges(Select.NEW)
            chamfer(newe2, 0.3)

            RigidJoint(  # to plate handle shaft
                "j1",
                joint_location=Location(
                    Plane(Face(Wire(newe2)).center(), z_dir=(0, 1, 0))
                ),
            )

            RigidJoint(  # to diamond plate holder
                "j2",
                joint_location=-Location(),  # NOTE: inverted loc
            )

        super().__init__(
            part=p_plate_holder_handle.part, rotation=rotation, align=align, mode=mode
        )

        # 2. Capture all local variables from this __init__ frame
        self.capture_debug_locals()

        # 3. Optionally show immediately if debug flag was passed
        if debug:
            self.show_debug()


if __name__ == "__main__":
    from sharp123 import create_assembly_config

    par = create_assembly_config()
    plate_holder_handle = PlateHolderHandle(par)
    plate_holder_handle.show_debug(render_joints=True)
