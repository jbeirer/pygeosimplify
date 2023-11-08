from typing import Any, List, Optional

import numpy as np
import pandas as pd
from distinctipy import get_colors
from mpl_toolkits.mplot3d import Axes3D

import pygeosimplify as pgs
from pygeosimplify.coordinate.definitions import XYZ, EtaPhiR, EtaPhiZ
from pygeosimplify.geo.base import Cell
from pygeosimplify.geo.cells import EtaPhiRCell, EtaPhiZCell, XYZCell
from pygeosimplify.vis.scene import CellScene


def plot_geometry(
    df: pd.DataFrame,
    ax: Axes3D = None,
    layer_list: Optional[List[int]] = None,
    color_list: Optional[Any] = None,
    eta_range: Optional[List] = None,
    phi_range: Optional[List] = None,
    axis_labels: Optional[List] = None,
    unit_scale: float = 1,
) -> Axes3D:
    """
    Plots the detector cells from pandas data frame

    Parameters:
    df (pd.DataFrame): The pandas DataFrame containing information about the layers, coordinates, and dimensions of cells.
    ax (Axes3D, optional): The 3D axes to plot on. If None, a new figure is created.
    layer_list (List[int], optional): The list of layers to plot. If None, all layers are plotted.
    color_list (List[Tuple[float, float, float]] | str, optional): The list of colors to use for each layer. If a string is provided, a default color scheme is used.
    eta_range (List, optional): The range of eta values to plot.
    phi_range (List, optional): The range of phi values to plot.
    axis_labels (List, optional): The labels for the x, y, and z axes.
    unit_scale (int, optional): Scaling factor to change units of dimensionful quantities.

    Returns:
    Axes3D: The 3D axes containing the plot.
    """
    if layer_list is None:
        layer_list = list(df["layer"].unique())
    if color_list is None:
        color_list = get_colors(len(layer_list), rng=0)
    if eta_range is None:
        eta_range = [-5, 5]
    if phi_range is None:
        phi_range = [0, np.pi]
    if axis_labels is None:
        axis_labels = ["x", "y", "z"]

    # Filter for eta and phi range
    df = filter_df_eta_phi(df, eta_range, phi_range)

    vis = CellScene()

    for color_idx, layer_idx in enumerate(layer_list):
        # Filter for layer
        layer_cells = df[(df["layer"] == layer_idx)]
        add_layer_cells_to_scene(layer_cells, vis, color_idx, unit_scale, color_list)

    ax = vis.plot(ax=ax, axis_labels=axis_labels)

    # Regularize x,y limits so that limits are identical for x and y (to avoid distortions)
    minMaxX = vis.min_max_cell_list_extent(0)
    minMaxY = vis.min_max_cell_list_extent(1)
    minMax = [min(minMaxX[0], minMaxY[0]), max(minMaxX[1], minMaxY[1])]
    ax.set_xlim(minMax)
    ax.set_ylim(minMax)

    return ax


def filter_df_eta_phi(df: pd.DataFrame, eta_range: List, phi_range: List) -> pd.DataFrame:
    # Filter for eta range
    df = df[(df["eta"] > eta_range[0]) & (df["eta"] < eta_range[1])]
    # Filter for phi range
    df = df[(df["phi"] > phi_range[0]) & (df["phi"] < phi_range[1])]

    return df


def add_layer_cells_to_scene(
    df: pd.DataFrame, scence: CellScene, color_idx: int, unit_scale: float, color_list: List
) -> None:
    for row in df.itertuples():
        cell = get_cell_from_row(row, unit_scale)
        scence.add_cell(cell, facecolor=color_list[color_idx], alpha=0.1, edgewidth=0.01)


def get_cell_from_row(row: pd.DataFrame, unit_scale: float) -> Cell:
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
