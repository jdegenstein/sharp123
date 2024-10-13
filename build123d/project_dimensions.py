# %%

from dataclasses import dataclass

# TODO: consider immutability


@dataclass
class ProjectDimensions:
    # x: float
    # most of the dimensional data will be in nested dataclasses:
    # trying alphabetical order:
    angle_adjustment_nut: "AngleAdjustmentNut"
    angle_adjustment_screw: "AngleAdjustmentScrew"
    base_plate: "BasePlate"
    clamp_arm: "ClampArm"
    clamp_arm_holder: "ClampArmHolder"
    clamping_screw: "ClampingScrew"
    diamond_plate_holder: "DiamondPlateHolder"
    plate_holder_handle: "PlateHolderHandle"
    small_parts: "SmallParts"
    tapered_clamping_nut: "TaperedClampingNut"


# trying alphabetical order:
@dataclass
class AngleAdjustmentNut:
    # just placeholder dimensions below
    internal_width: float = 80


@dataclass
class AngleAdjustmentScrew:
    # just placeholder dimensions below
    internal_width: float = 80


@dataclass
class BasePlate:
    # just placeholder dimensions below
    internal_width: float = 80


@dataclass
class ClampArm:
    # just placeholder dimensions below
    internal_width: float = 40


@dataclass
class ClampArmHolder:
    # just placeholder dimensions below
    internal_width: float = 80
    external_width: float = 100
    octagon_diameter: float = 40
    octagon_length: float = 60


@dataclass
class ClampingScrew:
    # just placeholder dimensions below
    internal_width: float = 80


@dataclass
class DiamondPlateHolder:
    # just placeholder dimensions below
    internal_width: float = 80


@dataclass
class PlateHolderHandle:
    # just placeholder dimensions below
    internal_width: float = 80


@dataclass
class SmallParts:
    # just placeholder dimensions below
    internal_width: float = 80


@dataclass
class TaperedClampingNut:
    # just placeholder dimensions below
    internal_width: float = 80


project_dimensions = ProjectDimensions(
    angle_adjustment_nut=AngleAdjustmentNut(),
    angle_adjustment_screw=AngleAdjustmentScrew(),
    base_plate=BasePlate(),
    clamp_arm=ClampArm(),
    clamp_arm_holder=ClampArmHolder(),
    clamping_screw=ClampingScrew(),
    diamond_plate_holder=DiamondPlateHolder(),
    plate_holder_handle=PlateHolderHandle(),
    small_parts=SmallParts(),
    tapered_clamping_nut=TaperedClampingNut(),
)
