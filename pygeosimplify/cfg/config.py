import inspect

import pygeosimplify.coordinate.definitions as coord_defs

# Get list of implemented coordinate systems
allowed_coordinate_systems = [name for name, obj in inspect.getmembers(coord_defs) if inspect.isclass(obj)]

coordinate_branch_names = {}


def set_coordinate_branch(coordinateSystem: str, branchName: str) -> None:
    if coordinateSystem not in allowed_coordinate_systems:
        raise ValueError(
            f"Coordinate system {coordinateSystem} is not supported. Supported coordinate systems are"
            f" {allowed_coordinate_systems}"
        )

    coordinate_branch_names[coordinateSystem] = branchName
