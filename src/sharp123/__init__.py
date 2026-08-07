from .build_parameters import BuildParameters
from .debug import DebugMixin
from .project_dimensions import create_assembly_config
from .parts import (
    Tower,
    BasePlate,
    ClampArmHolder,
    ClampingScrew,
    TaperedClampingNut,
    LongPin,
    PlateHandleShaft,
    PlateHolderHandle,
    Washer,
    ClampArm,
    AngleAdjustmentScrew,
    AngleAdjustmentNut,
    DiamondPlateHolder,
    AAScrewKey,
    KnifeExample,
)

__all__ = [
    "BuildParameters",
    "DebugMixin",
    "create_assembly_config",
    "Tower",
    "BasePlate",
    "ClampArmHolder",
    "ClampingScrew",
    "TaperedClampingNut",
    "LongPin",
    "PlateHandleShaft",
    "PlateHolderHandle",
    "Washer",
    "ClampArm",
    "AngleAdjustmentScrew",
    "AngleAdjustmentNut",
    "DiamondPlateHolder",
    "AAScrewKey",
    "KnifeExample",
    # TODO: add parts
    # TODO: add assembly?
]
