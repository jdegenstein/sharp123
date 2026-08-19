# %%
# project_dimensions.py
from sharp123 import BuildParameters


def create_assembly_config(
    # pcb_len: float = 100.0, # TODO: consider adding inputs, if necessary
) -> BuildParameters:
    """Generates a frozen BuildParameters tree with nested sub-namespaces."""
    with BuildParameters() as par:
        par.clearance = 0.3  # default clearance value

        # Sub-context: base plate, the only fixed object
        with BuildParameters() as base_plate:
            base_plate.cutout_len = 65
            base_plate.trap_width = 100
            base_plate.trap_height = 10
            base_plate.trap_angle = 45

        # Sub-context: main tower
        with BuildParameters() as tower:
            tower.trap_width = 100 - par.clearance
            tower.trap_height = 10 + par.clearance
            tower.trap_angle = 45
            tower.octagon_dia = 50

        # Sub-context: clamp arm holder
        with BuildParameters() as clamp_arm_holder:
            clamp_arm_holder.interior_width = tower.trap_width - 20
            clamp_arm_holder.octagon_dia = tower.octagon_dia - 3*par.clearance # loose fit
            clamp_arm_holder.pin_dia = 8
            clamp_arm_holder.pin_dia_hole = clamp_arm_holder.pin_dia + 0.6

        # Sub-context: small parts
        with BuildParameters() as small_parts:
            small_parts.pin_chamfer = 1

        # Sub-context: main tower
        with BuildParameters() as angle_screw:
            angle_screw.captured_length = 86

    return par


if __name__ == "__main__":
    par = create_assembly_config()
