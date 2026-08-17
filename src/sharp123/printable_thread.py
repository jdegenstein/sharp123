from build123d import *
from ocp_vscode import *
from bd_warehouse.thread import TrapezoidalThread, MetricTrapezoidalThread
from typing import Literal

class PrintableMetricTrapezoidalThread(TrapezoidalThread):
    """
    Metric Trapezoidal Thread tailored for 3D printing.
    Applies a radial clearance offset exclusively to internal threads.
    """

    @classmethod
    def sizes(cls) -> list[str]:
        return MetricTrapezoidalThread.standard_sizes

    def __init__(
        self,
        size: str,
        length: float,
        external: bool = True,
        clearance: float = 0.2,  # Radial clearance in mm for 3D printing
        hand: Literal["right", "left"] = "right",
        end_finishes: tuple[
            Literal["raw", "square", "fade", "chamfer"],
            Literal["raw", "square", "fade", "chamfer"],
        ] = ("fade", "fade"),
        interference: float = 0.2,
        rotation: RotationLike = (0, 0, 0),
        align: None | Align | tuple[Align, Align, Align] = None,
        mode: Mode = Mode.ADD,
    ):
        if size not in MetricTrapezoidalThread.standard_sizes:
            raise ValueError(
                f"size invalid, must be one of {MetricTrapezoidalThread.standard_sizes}"
            )

        nominal_diameter, pitch = (float(part) for part in size.split("x"))

        # Apply radial clearance ONLY to internal threads (nuts)
        effective_diameter = nominal_diameter
        if not external:
            # Increasing the diametral value by 2x clearance pushes 
            # the entire thread profile outward radially by the clearance amount.
            effective_diameter += (2 * clearance)

        super().__init__(
            diameter=effective_diameter,
            pitch=pitch,
            thread_angle=30.0,
            length=length,
            external=external,
            starts=1,
            hand=hand,
            end_finishes=end_finishes,
            interference=interference,
            rotation=rotation,
            align=align,
            mode=mode,
        )

if __name__ == "__main__":
    mtt = PrintableMetricTrapezoidalThread("14x3", 20, external=False, clearance=0.7)
    show(mtt)