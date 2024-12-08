# supported coordinate systems
allowed_coordinate_systems = ["XYZ", "EtaPhiR", "EtaPhiZ", "RPhiZ"]
# List of branches that are always required to be available
required_branches = ["eta", "phi", "layer", "r", "z", "isBarrel"]
# Dictionary mapping coordinate system to coordinate branch name, e.g. {"XYZ": "isCartesian"}
coordinate_branch_names = {}  # type: dict[str, str]


def reset_coordinate_branches() -> None:
    global coordinate_branch_names
    global required_branches

    coordinate_branch_names = {}
    required_branches = ["eta", "phi", "layer", "r", "z", "isBarrel"]


def set_coordinate_branch(coordinate_system: str, branch_name: str) -> None:
    global coordinate_branch_names
    global required_branches

    if coordinate_system not in allowed_coordinate_systems:
        raise ValueError(
            f"Coordinate system {coordinate_system} is not supported. Supported coordinate systems are"
            f" {allowed_coordinate_systems}"
        )

    coordinate_branch_names[coordinate_system] = branch_name

    required_branches.append(branch_name)

    # Add required branches depending on the set coordinate system
    if "XYZ" in coordinate_system:
        required_branches += ["x", "y", "z", "dx", "dy", "dz"]
    elif "EtaPhiR" in coordinate_system:
        required_branches += ["eta", "phi", "r", "deta", "dphi", "dr"]
    elif "EtaPhiZ" in coordinate_system:
        required_branches += ["eta", "phi", "z", "deta", "dphi", "dz"]
    elif "RPhiZ" in coordinate_system:
        required_branches += ["r", "phi", "z", "dr", "dphi", "dz"]


def set_coordinate_branch_dict(coordinate_branch_dict: dict) -> None:
    global coordinate_branch_names
    global required_branches

    reset_coordinate_branches()

    for coordinate_system in coordinate_branch_dict:
        if coordinate_system not in allowed_coordinate_systems:
            raise ValueError(
                f"Coordinate system {coordinate_system} is not supported. Supported coordinate systems are"
                f" {allowed_coordinate_systems}"
            )

    coordinate_branch_names = coordinate_branch_dict

    required_branches += list(coordinate_branch_dict.values())

    # Add required branches depending on the set coordinate system
    for coordinate_system in coordinate_branch_dict:
        if "XYZ" in coordinate_system:
            required_branches += ["x", "y", "z", "dx", "dy", "dz"]
        elif "EtaPhiR" in coordinate_system:
            required_branches += ["eta", "phi", "r", "deta", "dphi", "dr"]
        elif "EtaPhiZ" in coordinate_system:
            required_branches += ["eta", "phi", "z", "deta", "dphi", "dz"]
        elif "RPhiZ" in coordinate_system:
            required_branches += ["r", "phi", "z", "dr", "dphi", "dz"]
