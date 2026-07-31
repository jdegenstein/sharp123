# %%
from build123d import *
from ocp_vscode import *

show_clear()
set_defaults(ortho=True, default_edgecolor="#121212")
# %%
from sharp123 import BuildParameters, DebugMixin


# TODO: parameterize and check against other parts
class Tower(BasePartObject, DebugMixin):
    def __init__(
        self,
        par: BuildParameters,
        debug: bool = False,
        rotation: RotationLike = Rotation(0, 0, 0),
        align: tuple[Align, Align, Align] = (Align.CENTER, Align.CENTER, Align.CENTER),
        mode: Mode = Mode.ADD,
    ):
        with BuildPart() as p_tower:
            tower_ht = 180
            with BuildSketch() as s:
                Rectangle(par.tower.trap_width, tower_ht)
                fillet(vertices().group_by(Axis.Y)[0], 15)
            extrude(amount=par.base_plate.cutout_len / 2, both=True)
            with BuildSketch() as s2:
                add(s.sketch)
                split(bisect_by=Plane.XZ)
                offset(amount=-12)
            extrude(amount=par.base_plate.cutout_len / 2, both=True, mode=Mode.SUBTRACT)
            with BuildSketch() as s:
                RegularPolygon(
                    par.tower.octagon_dia / 2,
                    8,
                    rotation=360 / 8 / 2,
                    align=(Align.CENTER, Align.MIN),
                )
            extrude(amount=par.base_plate.cutout_len / 2, both=True, mode=Mode.SUBTRACT)
            vtx = (
                vertices().group_by(Axis.Y)[-1].group_by(Axis.X)[-1].sort_by(Axis.Z)[-1]
            )
            vtxt = (vtx.X, vtx.Y, 0)
            with BuildSketch() as s:
                with BuildLine() as l:
                    m1 = PolarLine(
                        (par.tower.trap_width / 2, tower_ht / 2),
                        par.tower.trap_height,
                        -90 - par.tower.trap_angle,
                        length_mode=LengthMode.VERTICAL,
                    )
                    m2 = Line(m1 @ 0, ((m1 @ 0).X, (m1 @ 1).Y))
                    m3 = Line(m2 @ 1, m1 @ 1)
                make_face()
                mirror(about=Plane.YZ)
            extrude(amount=par.base_plate.cutout_len / 2, both=True, mode=Mode.SUBTRACT)

            sel = faces().sort_by(Axis.Z)[-1].edges().sort_by(Axis.Y)[-1]

            RigidJoint(  # to base plate
                label="j1",
                joint_location=Location(Plane(sel @ 0.5, (-1, 0, 0), (0, 0, 1))),
            )

            sel2 = faces().sort_by(Axis.Z)[0].inner_wires().sort_by(SortBy.LENGTH)[0]
            sel2c = Face(sel2).center()
            RigidJoint(  # to clamp arm holder
                label="j2",
                joint_location=Location(Plane(sel2c, (1, 0, 0), (0, 0, 1))),
            )

        super().__init__(part=p_tower.part, rotation=rotation, align=align, mode=mode)

        # 2. Capture all local variables from this __init__ frame
        self.capture_debug_locals()

        # 3. Optionally show immediately if debug flag was passed
        if debug:
            self.show_debug()


if __name__ == "__main__":
    from sharp123 import create_assembly_config

    par = create_assembly_config()
    tower = Tower(par)
    tower.show_debug(render_joints=True)
    # set_colormap(ColorMap.golden_ratio())
    # # fmt: off
    # show_all(
    #     classes = [BuildPart, BuildSketch, BuildLine, ],  # comment to show all objects
    #     include = ["p_tower", ],
    #     exclude = ["", ],
    #     show_locals = False,
    #     helper_scale = 1,  # controls size of e.g. planes and axes
    # )  # fmt: on
