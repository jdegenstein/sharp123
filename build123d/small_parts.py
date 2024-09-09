# %%
from build123d import *
from ocp_vscode import *
from inspect import currentframe as cf

set_port(3939)
show_clear()
set_defaults(ortho=True, default_edgecolor="#121212")
# %%

# below dimensions are ALL guesses
short_pin_len = 25
short_pin_d = 8

long_pin_len = 100
long_pin_d = 8

pin_chamfer = 1

# for diamond plate carriage
shaft_len = 200
shaft_d = 10

washer_od = 25
washer_id = 8
washer_th = 4

with BuildPart() as p_short_pin:
    with BuildSketch() as s_short_pin:
        Circle(short_pin_d / 2)  # circular or regular polygon?
    extrude(amount=short_pin_len)
    chamfer(edges(), pin_chamfer)

with BuildPart() as p_long_pin:
    with BuildSketch() as s_long_pin:
        Circle(long_pin_d / 2)  # circular or regular polygon?
    extrude(amount=long_pin_len)
    chamfer(edges(), pin_chamfer)

with BuildPart() as p_shaft:
    with BuildSketch() as s_shaft:
        RegularPolygon(shaft_d / 2, 6)
    extrude(amount=shaft_len)
    chamfer(edges(), pin_chamfer)

with BuildPart() as p_washer:
    with BuildSketch() as s_washer:
        Circle(washer_od / 2)
        Circle(washer_id / 2, mode=Mode.SUBTRACT)
    extrude(amount=washer_th)

# TODO: add rectangular shaft retainer that will be used to retain angle adjustment screw

packed = pack(
    [p_short_pin.part, p_long_pin.part, p_shaft.part, p_washer.part],
    padding=5,
    align_z=True,
)

show(packed)
