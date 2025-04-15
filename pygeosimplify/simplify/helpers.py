from itertools import combinations

import numpy as np
import pandas as pd
from pyg4ometry.geant4 import LogicalVolume, Material, MaterialPredefined, PhysicalVolume
from pyg4ometry.geant4.Registry import Registry
from pyg4ometry.geant4.solid import Box, Tubs

from pygeosimplify.simplify.cylinder import Cylinder


def init_world(material: Material, X: float = 40000, Y: float = 40000, Z: float = 80000) -> tuple[Box, Registry]:
    # registry to store gdml data
    reg = Registry()

    # world solid and logical
    world_solid = Box("World_Solid", X, Y, Z, reg)
    world_logic = LogicalVolume(world_solid, material, "WorldLog", reg)
    reg.setWorld(world_logic.name)

    return world_logic, reg


def check_world_overlap(
    world: Box, print_output: bool = True, recursive: bool = False, coplanar: bool = False
) -> tuple[int, list[str]]:
    """
    Check for overlaps in the world volume using the logging-based approach of newer pyg4ometry.

    Args:
        world: The logical volume to check
        print_output: Whether to print the captured output
        recursive: Whether to check recursively
        coplanar: Whether to check for coplanar overlaps

    Returns:
        Tuple of (number of overlaps, list of overlapping volume names)
    """
    import io
    import logging
    import re

    # Reset overlap check status
    world.overlapChecked = False

    # Create a capture for logging
    log_capture = io.StringIO()
    log_handler = logging.StreamHandler(log_capture)

    # Get pyg4ometry logger
    logger = logging.getLogger("pyg4ometry")

    # Store original configuration
    original_handlers = logger.handlers.copy()
    original_level = logger.level

    # Set up logging capture
    logger.handlers = [log_handler]
    logger.setLevel(logging.DEBUG)  # Capture all log levels

    try:
        # Initialize overlap counter
        overlap_count = [0]

        # Run the overlap check
        world.checkOverlaps(recursive=recursive, coplanar=coplanar, nOverlapsDetected=overlap_count)

        # Get the number of overlaps directly from the counter
        n_overlaps = overlap_count[0]

        # Get the log output
        log_output = log_capture.getvalue()

        if print_output:
            print(log_output)

        # Extract overlap pairs using regex
        # Look for the specific error message format that indicates overlaps
        overlap_pairs = []

        # Find all overlap lines
        overlap_lines = re.findall(
            r"OVERLAP DETECTED> overlap between daughters of .*? (Layer_.*?_Phys) (Layer_.*?_Phys)", log_output
        )

        for pair in overlap_lines:
            # Extract the actual layer names without the "Layer_" prefix and "_Phys" suffix
            first = re.search(r"Layer_(.*?)_Phys", pair[0]).group(1)
            second = re.search(r"Layer_(.*?)_Phys", pair[1]).group(1)
            overlap_pairs.append([first, second])

        return n_overlaps, overlap_pairs

    finally:
        # Restore original logger configuration
        logger.handlers = original_handlers
        logger.setLevel(original_level)


def check_pairwise_overlaps(
    cyl_dict: dict[str, Cylinder], print_output: bool = True, recursive: bool = False, coplanar: bool = False
) -> tuple[int, list[list[str]]]:
    """
    Check for pairwise overlaps between cylinders.

    Args:
        cyl_dict: Dictionary of cylinders to check
        print_output: Whether to print the captured output
        recursive: Whether to check recursively
        coplanar: Whether to check for coplanar overlaps

    Returns:
        Tuple of (number of overlaps, list of overlapping volume names)
    """

    layer_pairs = list(combinations(cyl_dict.keys(), 2))
    n_total_overlaps = 0
    total_overlap_list = []
    for pair in layer_pairs:
        cyl_name_a, cyl_name_b = pair[0], pair[1]
        cyl_a, cyl_b = cyl_dict[cyl_name_a], cyl_dict[cyl_name_b]

        # Build a test dictionary containing two cylinders to test for overlaps
        cyl_test_dict = {cyl_name_a: cyl_a, cyl_name_b: cyl_b}

        n_overlaps, overlap_list = check_cyl_dict_overlaps(cyl_test_dict, print_output, recursive, coplanar)

        if n_overlaps > 0:
            n_total_overlaps += n_overlaps
            for pair in overlap_list:
                if pair not in total_overlap_list:
                    total_overlap_list.append(pair)

    return n_total_overlaps, total_overlap_list


def add_cylinder_to_reg(name: str, registry: Registry, world: Box, cyl: Cylinder, material: Material) -> None:
    """! Adds a cylinder positioned around the z-axis defined by minimum and maximum R / Z values to the registry.
    Note: zmin, zmax can be negative.
    """

    if cyl.zmin > cyl.zmax:
        raise Exception(f"zmin > zmax for cylinder {name}, zmin = {cyl.zmin}, zmax = {cyl.zmax}")

    if cyl.rmin > cyl.rmax:
        raise Exception(f"rmin > rmax for cylinder {name}, rmin = {cyl.rmin}, rmax = {cyl.rmax}")

    # The centre position of the cylinder
    zCentre = cyl.zmin + 0.5 * (cyl.zmax - cyl.zmin)
    position = [0, 0, zCentre]
    # Longitudinal width of the cylinder
    deltaZ = cyl.zmax - cyl.zmin

    solid = Tubs(f"Layer_{name}_Solid", cyl.rmin, cyl.rmax, deltaZ, 0, 2 * np.pi, registry, addRegistry=True)
    logic = LogicalVolume(solid, material, f"Layer_{name}_Log", registry, addRegistry=True)
    PhysicalVolume([0, 0, 0], position, logic, f"Layer_{name}_Phys", world, registry, addRegistry=True)


def add_cylinder_dict_to_reg(registry: Registry, world_log: LogicalVolume, cyl_dict: dict, material: Material) -> None:
    for idx in cyl_dict:
        cyl = cyl_dict[idx]
        add_cylinder_to_reg(idx, registry, world_log, cyl, material)


def check_cyl_dict_overlaps(
    cyl_dict: dict, print_output: bool = True, recursive: bool = False, coplanar: bool = False
) -> tuple[int, list[str]]:
    """
    Check for overlaps in a dictionary of cylinders.

    Args:
        cyl_dict: Dictionary of cylinders to check
        print_output: Whether to print the captured output
        recursive: Whether to check recursively
        coplanar: Whether to check for coplanar overlaps

    Returns:
        Tuple of (number of overlaps, list of overlapping volume names)
    """

    material = MaterialPredefined("G4_Galactic")
    world_logic, reg = init_world(material)

    # Add cylinders to the registry
    add_cylinder_dict_to_reg(reg, world_logic, cyl_dict, material)

    # Check for overlaps
    n_overlaps, overlap_list = check_world_overlap(world_logic, print_output, recursive, coplanar)

    return n_overlaps, overlap_list


def overlap_distance(min1: float, max1: float, min2: float, max2: float) -> float:
    return max(0, min(max1, max2) - max(min1, min2))


def z_overlap_filter(row: pd.DataFrame, z_min_test: float, z_max_test: float) -> bool:
    """! Decides wether the line spanned by zmin and zmax overlaps with the line spanned by zMinTest and zMaxTest
    by computing the overlap distance between both
    """
    overlapDistance = overlap_distance(row.zmin, row.zmax, z_min_test, z_max_test)

    return overlapDistance > 0


def r_overlap_filter(row: pd.DataFrame, r_min_test: float, r_max_test: float) -> bool:
    """! Decides wether the line spanned by rmin and rmax overlaps with the line spanned by rMinTest and rMaxTest
    by computing the overlap distance between both
    """
    overlapDistance = overlap_distance(row.rmin, row.rmax, r_min_test, r_max_test)

    return overlapDistance > 0
