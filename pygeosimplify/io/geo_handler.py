import pandas as pd
import uproot

import pygeosimplify.cfg.config as config


def tree_to_df(tree: uproot.models.TTree) -> pd.DataFrame:
    """
    Convert a ROOT TTree to a pandas DataFrame.

    Parameters:
    tree (uproot.models.TTree): The ROOT TTree to convert.

    Returns:
    pd.DataFrame: The resulting pandas DataFrame.
    """
    df = tree.arrays(tree.keys(), library="pd")

    return df


def load_geometry(file_path: str, tree_name: str) -> pd.DataFrame:
    """
    Load geometry from a ROOT file into a pandas DataFrame.

    Args:
        file_path (str): The path to the ROOT file.
        tree_name (str): The name of the tree to load.

    Returns:
        pd.DataFrame: A pandas DataFrame containing the loaded geometry.

    Raises:
        Exception: If coordinate branches have not been set before loading geometry.
    """
    if config.coordinate_branch_names == {}:
        raise Exception(
            "Coordinate branches have not been set. Please set coordinate branches before loading geometry."
        )
    # Open root tree with uprot
    tree = uproot.open(f"{file_path}:{tree_name}")
    # Convert the tree to a pandas dataframe
    df = tree_to_df(tree)
    # Check whether the tree contains all required branches
    check_geo_consistency(df)

    return df


def check_geo_consistency(df: pd.DataFrame) -> None:
    """
    Check the consistency of the provided geo data.

    Args:
        df (pd.DataFrame): A pandas DataFrame containing the geo data.

    Raises:
        Exception: If any of the required branches are missing in the DataFrame.
        Exception: If any cell has none or multiple coordinate systems assigned.
        Exception: If not all cells in a layer have the same coordinate system assigned.
    """
    # Check whether all required branches are available in the tree
    for required_branch in config.required_branches:
        if required_branch not in df.columns:
            raise Exception(
                f"Required branch {required_branch} not found in tree. Please provide a tree containing all required"
                f" branches: {config.required_branches}"
            )

    # Cross check that each cell has exactly one coordinate system assigned
    coordinate_columns = df[config.coordinate_branch_names.values()]
    checksum = coordinate_columns.sum(axis=1)
    if not checksum.all() == 1:
        raise Exception(
            "Cells have none or multiple coordinate systems assigned. Coordinate branches are:"
            f" {config.coordinate_branch_names}"
        )
    # Cross check that for each layer, all cells have the same coordinate system assigned
    for layer_idx in df["layer"].unique():
        layer_df = df[df["layer"] == layer_idx]
        coordinate_columns = layer_df[config.coordinate_branch_names.values()]

        # get the coordinate system column
        unique_columns_check = coordinate_columns == 1
        layer_coordinate_system_column = coordinate_columns.columns[unique_columns_check.all()]

        # exactly one column where all cells have identical layer coordinate system
        if not len(layer_coordinate_system_column) == 1:
            raise Exception(f"Not all cells in layer {layer_idx} have the same coordinate system assigned.")
