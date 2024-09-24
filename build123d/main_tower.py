# %%
from build123d import *
from ocp_vscode import *
from inspect import currentframe as cf

set_port(3939)
show_clear()
set_defaults(ortho=True, default_edgecolor="#121212")
# %%


# TODO: parameterize and check against other parts

with BuildPart() as p_tower:
    with BuildSketch() as s:
        Rectangle(100, 180)
        fillet(vertices().group_by(Axis.Y)[0], 15)
    extrude(amount=50 / 2, both=True)
    with BuildSketch() as s2:
        add(s.sketch)
        split(bisect_by=Plane.XZ)
        offset(amount=-12)
    extrude(amount=50 / 2, both=True, mode=Mode.SUBTRACT)
    with BuildSketch() as s:
        RegularPolygon(50 / 2, 8, rotation=360 / 8 / 2, align=(Align.CENTER, Align.MIN))
    extrude(amount=50 / 2, both=True, mode=Mode.SUBTRACT)
    vtx = vertices().group_by(Axis.Y)[-1].group_by(Axis.X)[-1].sort_by(Axis.Z)[-1]
    vtxt = (vtx.X,vtx.Y,0)
    with BuildSketch() as s:
        with BuildLine() as l:
            m1 = PolarLine(vtxt,12,-120)
            m2 = Line(m1@0,((m1@0).X,(m1@1).Y))
            m3 = Line(m2@1,m1@1)
        make_face()
        mirror(about=Plane.YZ)
    extrude(amount=50 / 2, both=True, mode=Mode.SUBTRACT)
    
# print(f"\npart mass = {p.part.volume*densa}")
classes = (BuildPart, BuildSketch, BuildLine)  # for OCP-vscode
set_colormap(ColorMap.seeded(colormap="rgb", alpha=1, seed_value="vscod"))
variables, s_o, s_n, slocal = (list(cf().f_locals.items()), [], [], False)
for name, obj in variables:
    if (
        isinstance(obj, classes)
        and not name.startswith("_")
        and not name.startswith("obj")
        and not obj._obj is None
    ):
        if obj._obj_name != "sketch" or slocal:
            s_o.append(obj), s_n.append(f"{name}.{obj._obj_name}")
        elif obj._obj_name == "sketch":
            s_o.append(obj.sketch), s_n.append(f"{name}.{obj._obj_name}")
show(
    *s_o,
    vtx,
    names=s_n,
    reset_camera=Camera.KEEP,
)
