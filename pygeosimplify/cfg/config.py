# supported coordinate systems
allowed_coordinate_systems = ["XYZ", "EtaPhiR", "EtaPhiZ"]
# List of branches that are required to be available
required_branches = ["eta", "phi", "layer"]

coordinate_branch_names = {}


def set_coordinate_branch(coordinate_system: str, branch_name: str) -> None:
    global coordinate_branch_names

    if coordinate_system not in allowed_coordinate_systems:
        raise ValueError(
            f"Coordinate system {coordinate_system} is not supported. Supported coordinate systems are"
            f" {allowed_coordinate_systems}"
        )

    coordinate_branch_names[coordinate_system] = branch_name


def set_coordinate_branch_dict(coordinate_branch_dict: dict) -> None:
    global coordinate_branch_names

    for coordinate_system in coordinate_branch_dict:
        if coordinate_system not in allowed_coordinate_systems:
            raise ValueError(
                f"Coordinate system {coordinate_system} is not supported. Supported coordinate systems are"
                f" {allowed_coordinate_systems}"
            )

    coordinate_branch_names = coordinate_branch_dict
