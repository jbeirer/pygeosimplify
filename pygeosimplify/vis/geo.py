from typing import Any

import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from distinctipy import get_colors
from mpl_toolkits.mplot3d import Axes3D

import pygeosimplify as pgs
from pygeosimplify.coordinate.definitions import XYZ, EtaPhiR, EtaPhiZ
from pygeosimplify.geo.base import Cell
from pygeosimplify.geo.cells import EtaPhiRCell, EtaPhiZCell, XYZCell
from pygeosimplify.vis.scene import CellScene


def plot_geometry(  # noqa: C901
    df: pd.DataFrame,
    ax: Axes3D = None,
    layer_list: list[int] | None = None,
    eta_range: list | None = None,
    phi_range: list | None = None,
    axis_labels: list | None = None,
    color: str | None = None,
    unit_scale: float = 1,
    cell_energy_col: str | None = None,
    unit_scale_energy: float = 1,
    energy_label: str = "Cell Energy",
    color_map: str = "gist_heat_r",
) -> Axes3D:
    """
    Plot the geometry based on the provided DataFrame.

    Parameters:
        df (pd.DataFrame): The DataFrame containing the geometry data.
        ax (Axes3D, optional): The 3D axes to plot on. If not provided, a new figure and axes will be created.
        layer_list (List[int], optional): The list of layers to consider. If not provided, all layers will be considered.
        eta_range (List, optional): The range of eta values to filter the data. If not provided, the default range is [-5, 5].
        phi_range (List, optional): The range of phi values to filter the data. If not provided, the default range is [0, np.pi].
        axis_labels (List, optional): The labels for the x, y, and z axes. If not provided, the default labels are ["x", "y", "z"].
        color (str, optional): The color to use for the cells. If not provided, colors will be automatically assigned based on the layers.
        unit_scale (float, optional): The scale factor for the unit of measurement. Default is 1.
        cell_energy_col (str, optional): The name of the column containing the cell energy values. If provided, the cells will be colored based on the energy values.
        unit_scale_energy (float, optional): The scale factor for the unit of measurement of the cell energy. Default is 1.
        energy_label (str, optional): The label for the colorbar when cell energy is used. Default is "Cell Energy".
        color_map (str, optional): The colormap to use when coloring the cells based on energy values. Default is "gist_heat_r".

    Returns:
        Axes3D: The 3D axes object containing the plot.
    """

    if ax is None:
        fig = plt.figure()
        ax = fig.add_subplot(111, projection="3d")

    if eta_range is None:
        eta_range = [-5, 5]
    if phi_range is None:
        phi_range = [0, np.pi]
    if axis_labels is None:
        axis_labels = ["x", "y", "z"]

    # If no layer list is provided consider all all layers
    if layer_list is None:
        layer_list = list(df["layer"].unique())

    # Filter for layer list
    df = df[df["layer"].isin(layer_list)]

    # Filter for eta and phi range
    df = filter_df_eta_phi(df, eta_range, phi_range)

    # Create a visual cell scene
    vis = CellScene()

    if not cell_energy_col:
        # Create a color dict mapping a layer to a color
        layer_color_dict = dict(zip(layer_list, get_colors(len(layer_list), rng=0), strict=False))
        # If color is specifically provided, override the color dict
        if color:
            layer_color_dict = {layer: color for layer in layer_list}
        add_cells_to_scene(
            df=df,
            scene=vis,
            unit_scale=unit_scale,
            layer_color_dict=layer_color_dict,
        )
    else:
        # Make sure the energy column exists
        if cell_energy_col not in df.columns:
            raise ValueError(f"Column {cell_energy_col} not found in DataFrame")
        # Make sure the energy column is not empty and not always 0
        if df[cell_energy_col].empty or df[cell_energy_col].eq(0).all():
            raise ValueError(f"Column {cell_energy_col} is empty or always 0")

        # Create a color map mapping cell energy to a color
        vmin = df[cell_energy_col].min() * unit_scale_energy
        vmax = df[cell_energy_col].max() * unit_scale_energy
        norm = mcolors.LogNorm(vmin * 0.1, vmax)

        add_cells_to_scene(
            df=df,
            scene=vis,
            unit_scale=unit_scale,
            unit_scale_energy=unit_scale_energy,
            colormap=plt.get_cmap(color_map),
            norm=norm,
        )

    vis.plot(ax=ax, axis_labels=axis_labels)

    if cell_energy_col:
        mappable = plt.cm.ScalarMappable(norm=norm, cmap=plt.get_cmap(color_map))
        cbar = plt.colorbar(mappable, ax=ax, fraction=0.035, pad=0.15)
        cbar.set_label(energy_label)

    # Regularize x,y limits so that limits are identical for x and y (to avoid distortions)
    minMaxX = vis.min_max_cell_list_extent(0)
    minMaxY = vis.min_max_cell_list_extent(1)
    minMax = [min(minMaxX[0], minMaxY[0]), max(minMaxX[1], minMaxY[1])]
    ax.set_xlim(minMax)
    ax.set_ylim(minMax)

    return ax


def filter_df_eta_phi(df: pd.DataFrame, eta_range: list, phi_range: list) -> pd.DataFrame:
    """
    Filter a DataFrame based on the given eta and phi ranges.

    Args:
        df (pd.DataFrame): The DataFrame to filter.
        eta_range (List): A list containing the minimum and maximum eta values.
        phi_range (List): A list containing the minimum and maximum phi values.

    Returns:
        pd.DataFrame: The filtered DataFrame.
    """
    # Filter for eta range
    df = df[(df["eta"] > eta_range[0]) & (df["eta"] < eta_range[1])]
    # Filter for phi range
    df = df[(df["phi"] > phi_range[0]) & (df["phi"] < phi_range[1])]

    return df


def add_cells_to_scene(
    df: pd.DataFrame,
    scene: CellScene,
    unit_scale: float,
    unit_scale_energy: float | None = 1,
    layer_color_dict: dict | None = None,
    colormap: Any | None = None,
    norm: mcolors.Normalize | None = None,
) -> None:
    """
    Adds cells to a given scene.

    Args:
        df (pd.DataFrame): The DataFrame containing the cell data.
        scene (CellScene): The scene to which the cells will be added.
        unit_scale (float): The scale factor for the cell units.
        unit_scale_energy (Optional[float], optional): The scale factor for the cell energy units. Defaults to 1.
        layer_color_dict (Optional[Dict], optional): A dictionary mapping layer names to colors. Defaults to None.
        colormap (Optional[Any], optional): The colormap used to map cell energy values to colors. Defaults to None.
        norm (Optional[mcolors.Normalize], optional): The normalization function used for the colormap. Defaults to None.
    """
    for row in df.itertuples():
        cell = get_cell_from_row(row, unit_scale)

        # Get color from color dict if provided, else use colormap
        if layer_color_dict:
            color = layer_color_dict[row.layer]
        else:
            if colormap is None or norm is None:
                raise ValueError("colormap and norm must be provided if layer_color_dict is not provided")

            color = colormap(norm(row.cell_energy * unit_scale_energy))

        scene.add_cell(cell, facecolor=color, alpha=0.1, edgewidth=0.01)


def get_cell_from_row(row: pd.DataFrame, unit_scale: float) -> Cell:
    """
    Converts a row of data into a Cell object based on the coordinate branch names.

    Args:
        row (pd.DataFrame): The row of data containing the coordinate information.
        unit_scale (float): The scaling factor to apply to the coordinate values.

    Returns:
        Cell: The corresponding Cell object based on the coordinate branch names.
    """
    if getattr(row, pgs.cfg.config.coordinate_branch_names["XYZ"]):
        cell = XYZCell(
            row.dx * unit_scale,
            row.dy * unit_scale,
            row.dz * unit_scale,
            XYZ(row.x * unit_scale, row.y * unit_scale, row.z * unit_scale),
        )
    elif getattr(row, pgs.cfg.config.coordinate_branch_names["EtaPhiR"]):
        cell = EtaPhiRCell(
            row.deta, row.dphi, row.dr * unit_scale, EtaPhiR(row.eta, row.phi, row.r * unit_scale)
        ).to_XYZ()
    elif getattr(row, pgs.cfg.config.coordinate_branch_names["EtaPhiZ"]):
        cell = EtaPhiZCell(
            row.deta, row.dphi, row.dz * unit_scale, EtaPhiZ(row.eta, row.phi, row.z * unit_scale)
        ).to_XYZ()

    return cell
