# %%
# project_dimensions.py
from sharp123 import BuildParameters

def create_assembly_config(
    pcb_len: float = 100.0,
    pcb_wid: float = 80.0,
    wall_thick: float = 3.0,
) -> BuildParameters:
    """Generates a frozen BuildParameters tree with nested sub-namespaces."""
    with BuildParameters() as par:
        par.clearance = 0.5
        par.wall_thickness = wall_thick
        par.fastener_diameter = 3.0  # M3 standard

        # Sub-context: PCB
        with BuildParameters() as pcb:
            pcb.length = pcb_len
            pcb.width = pcb_wid

        # Sub-context: Base Enclosure Box
        with BuildParameters() as box:
            box.internal_length = par.pcb.length + (2 * par.clearance)
            box.internal_width = par.pcb.width + (2 * par.clearance)
            box.outer_length = box.internal_length + (2 * par.wall_thickness)
            box.outer_width = box.internal_width + (2 * par.wall_thickness)
            box.height = 25.0

        # Sub-context: Lid
        with BuildParameters() as lid:
            lid.thickness = 4.0
            lid.lip_height = 2.0

        # Sub-context: Hardware
        with BuildParameters() as hardware:
            hardware.clearance_hole_radius = (par.fastener_diameter / 2) + 0.15
            hardware.standoff_height = 6.0
            hardware.standoff_radius = 3.5

    return par

if __name__ == "__main__":
    par = create_assembly_config()