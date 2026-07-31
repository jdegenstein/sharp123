# %%
from build123d import *
from ocp_vscode import *

show_clear()
set_defaults(ortho=True, default_edgecolor="#121212")
# %%
from sharp123 import BuildParameters, DebugMixin


class PartTemplate(BasePartObject, DebugMixin):
    def __init__(
        self,
        par: BuildParameters,
        debug: bool = False,
        rotation: RotationLike = Rotation(0, 0, 0),
        align: tuple[Align, Align, Align] = (Align.CENTER, Align.CENTER, Align.CENTER),
        mode: Mode = Mode.ADD,
    ):
        ___________

        super().__init__(part=___________, rotation=rotation, align=align, mode=mode)

        # 2. Capture all local variables from this __init__ frame
        self.capture_debug_locals()

        # 3. Optionally show immediately if debug flag was passed
        if debug:
            self.show_debug()


if __name__ == "__main__":
    from sharp123 import create_assembly_config

    par = create_assembly_config()
    part_template = PartTemplate(par)
    part_template.show_debug(render_joints=True)
