import pandas as pd
import uproot

import pygeosimplify.cfg.config as config


def load_geometry(file_path: str, tree_name: str) -> pd.DataFrame:
    if config.coordinate_branch_names == {}:
        raise Exception(
            "Coordinate branches have not been set. Please set coordinate branches before loading geometry."
        )

    tree = uproot.open(f"{file_path}:{tree_name}")

    # Check whether the promised branch names are available in the tree
    for promised_cs_branch in config.coordinate_branch_names.values():
        if promised_cs_branch not in tree.keys():
            raise Exception(
                f"Branch {promised_cs_branch} not found in tree {tree_name}. Please check whether the correct branch"
                " names have been provided."
            )

    # Add required branches depending on the set coordinate system
    if "XYZ" in config.coordinate_branch_names:
        config.required_branches += ["x", "y", "z", "dx", "dy", "dz"]
    if "EtaPhiR" in config.coordinate_branch_names:
        config.required_branches += ["eta", "phi", "r", "deta", "dphi", "dr"]
    if "EtaPhiZ" in config.coordinate_branch_names:
        config.required_branches += ["eta", "phi", "z", "deta", "dphi", "dz"]

    # Check whether all required branches are available in the tree
    for required_branch in config.required_branches:
        if required_branch not in tree.keys():
            raise Exception(
                f"Required branch {required_branch} not found in tree {tree_name}. Please provide a tree containing all"
                f" required branches: {config.required_branches}"
            )

    df = tree_to_df(tree)

    return df


def tree_to_df(tree: uproot.models.TTree) -> pd.DataFrame:
    df = tree.arrays(tree.keys(), library="pd")

    return df
