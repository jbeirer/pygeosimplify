import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from mpl_toolkits.mplot3d import Axes3D

from pygeosimplify.cfg import config
from pygeosimplify.coordinate.definitions import XYZ, EtaPhiR, EtaPhiZ, RPhiZ
from pygeosimplify.geo.cells import EtaPhiRCell, EtaPhiZCell, RPhiZCell, XYZCell
from pygeosimplify.simplify.cylinder import Cylinder
from pygeosimplify.vis.cylinder import plot_cylinder
from pygeosimplify.vis.geo import plot_geometry


class GeoLayer:
    """
    A class representing a layer of cells in a calorimeter.

    Attributes:
    -----------
    df : pd.DataFrame
        A pandas dataframe containing the cell information for the layer.
    layer_idx : int
        The index of the layer.
    coordinate_system : str
        The coordinate system used to represent the cell positions.
    is_barrel : bool
        True if the layer is a barrel layer, False otherwise.
    cells : List[Union[XYZCell, EtaPhiRCell, EtaPhiZCell, RPhiZCell]]
        A list of cell objects representing the cells in the layer.
    extent : dict
        A dictionary containing the minimum and maximum values of r and z coordinates of the cells in the layer.

    Methods:
    --------
    get_cell_envelope() -> Cylinder:
        Returns cylinder envelope of the cells in the layer.
    get_thinned_cylinder(layer_width: float = 10) -> dict:
        Returns cylinder constructed from thinned down version of the cells in the layer.
    plot_cell_centre_rz(ax: Union[None , plt.Axes] = None, color: Union[tuple[float, float, float], str] = 'tab:blue', marker_size: float = 0.01, x_label: str = 'z', y_label: str = 'r') -> plt.Axes:
        Plots the r-z coordinates of the cell centres in the layer.
    plot(ax: Axes3D = None, thinned: bool = False, color: Union[tuple[float, float, float], str] = 'red') -> Axes3D:
        Plots the cells in the layer in 3D space.
    is_continuous_in_z(distance_threshold: float = 50) -> bool:
        Checks whether the layer is approximately continuous in z around z=0.
    """

    def __init__(self, df: pd.DataFrame, layer_idx: int):
        """
        Initializes a GeoLayer object.

        Parameters:
        -----------
        df : pd.DataFrame
            A pandas dataframe containing the cell information for the layer.
        layer_idx : int
            The index of the layer.
        """
        self.df = df[df["layer"] == layer_idx]
        self.idx = str(layer_idx)
        self.coordinate_system = self._get_coordinate_system()
        self.is_barrel = self.df.isBarrel.all()
        self.cells = self._get_cells(self.df)
        self.extent = self._min_max_rz_extent(self.cells)
        self.thinned_cylinder = self.get_thinned_cylinder()

    def _get_coordinate_system(self) -> str:
        """
        Infers the coordinate system used to define the cells in the layer.

        Returns:
        --------
        str:
            The coordinate system used to define the cells in the layer.
        """
        for coordinate_system, branch_name in config.coordinate_branch_names.items():
            if self.df[branch_name].all() == 1:
                return coordinate_system
        raise Exception(f"Could not infer set coordinate system found for layer {self.idx}.")

    def _get_cells(self, df: pd.DataFrame) -> list[XYZCell] | list[EtaPhiRCell] | list[EtaPhiZCell] | list[RPhiZCell]:
        """
        Returns a list of cell objects representing the cells in the layer.

        Parameters:
        -----------
        df : pd.DataFrame
            A pandas dataframe containing the cell information for the layer.

        Returns:
        --------
        Union[List[XYZCell], List[EtaPhiRCell], List[EtaPhiZCell], List[RPhiZCell]]:
            A list of cell objects representing the cells in the layer.
        """
        if self.coordinate_system == "XYZ":
            return [
                XYZCell(dx, dy, dz, pos=XYZ(x, y, z))
                for dx, dy, dz, x, y, z in zip(df.dx, df.dy, df.dz, df.x, df.y, df.z, strict=False)
            ]
        elif self.coordinate_system == "EtaPhiR":
            return [
                EtaPhiRCell(deta, dphi, dr, pos=EtaPhiR(eta, phi, r))
                for deta, dphi, dr, eta, phi, r in zip(df.deta, df.dphi, df.dr, df.eta, df.phi, df.r, strict=False)
            ]
        elif self.coordinate_system == "EtaPhiZ":
            return [
                EtaPhiZCell(deta, dphi, dz, pos=EtaPhiZ(eta, phi, z))
                for deta, dphi, dz, eta, phi, z in zip(df.deta, df.dphi, df.dz, df.eta, df.phi, df.z, strict=False)
            ]
        elif self.coordinate_system == "RPhiZ":
            return [
                RPhiZCell(dr, dphi, dz, pos=RPhiZ(r, phi, z))
                for dr, dphi, dz, r, phi, z in zip(df.dr, df.dphi, df.dz, df.r, df.phi, df.z, strict=False)
            ]
        else:
            raise Exception(f"Invalid coordinate system {self.coordinate_system}.")

    def _cell_vertices_rz(
        self, cells: list[XYZCell] | list[EtaPhiRCell] | list[EtaPhiZCell] | list[RPhiZCell]
    ) -> tuple[list[float], list[float]]:
        """
        Returns the r and z values of the cell vertices in the layer.

        Parameters:
        -----------
        cells : Union[List[XYZCell], List[EtaPhiRCell], List[EtaPhiZCell], List[RPhiZCell]]
            A list of XYZ, EtaPhiR, EtaPhiZ or RPhiZCell cells.

        Returns:
        --------
        Tuple[List[float], List[float]]:
            A tuple containing the r and z values of cell vertices.
        """
        vertex_list = np.concatenate([cell.vertices for cell in cells], axis=0)

        if self.coordinate_system == "XYZ":
            z_values = [vertex.z for vertex in vertex_list]
            r_values = [vertex.to_RPhiZ().r for vertex in vertex_list]
        elif self.coordinate_system == "EtaPhiR":
            z_values = [vertex.to_XYZ().z for vertex in vertex_list]
            r_values = [vertex.r for vertex in vertex_list]
        elif self.coordinate_system == "EtaPhiZ":
            z_values = [vertex.z for vertex in vertex_list]
            r_values = [vertex.to_RPhiZ().r for vertex in vertex_list]
        elif self.coordinate_system == "RPhiZ":
            z_values = [vertex.z for vertex in vertex_list]
            r_values = [vertex.r for vertex in vertex_list]

        return r_values, z_values

    def _min_max_rz_extent(
        self, cells: list[XYZCell] | list[EtaPhiRCell] | list[EtaPhiZCell] | list[RPhiZCell]
    ) -> dict:
        """
        Returns a dictionary containing the minimum and maximum values of r and z coordinates of the cells in the layer.

        Parameters:
        -----------
        cells : Union[List[XYZCell], List[EtaPhiRCell], List[EtaPhiZCell], List[RPhiZCell]]
            A list of cell objects representing the cells in the layer.

        Returns:
        --------
        dict:
            A dictionary containing the minimum and maximum values of r and z coordinates of the cells in the layer.
        """
        r_values, z_values = self._cell_vertices_rz(cells)

        return {"rmin": min(r_values), "rmax": max(r_values), "zmin": min(z_values), "zmax": max(z_values)}

    def get_cell_envelope(self) -> Cylinder:
        """
        Returns minimal cylinder envelope that contains all cells in the layer.
        As the detector is assumed to be symmetric in +-z, the computation of the envelopes is based on the positive z halfspace, by convention.

        Returns:
        --------
        dict:
            Minimal cylinder envelope that contains all cells in the layer.
        """
        half_space_df = self.df[self.df.z > 0]

        cells = self._get_cells(half_space_df)

        cell_envelope = Cylinder(**self._min_max_rz_extent(cells), is_barrel=self.is_barrel)

        return cell_envelope

    def get_thinned_cylinder(self, layer_width: float = 10) -> Cylinder:
        """
        Returns a dictionary containing the cylinder definition of the thinned down version of the layer.
        For barrel layers the radius of the cylinder is thinned down, for endcap layers the z thickness of the cylinder is thinned down.

        Parameters:
        -----------
        layer_width : float, optional
            The width of the thinned down version of the cells in the layer, by default 10.

        Returns:
        --------
        dict:
            A dictionary containing the containing the cylinder definition of the thinned down versions of the layers
        """
        cyl = self.get_cell_envelope()

        if self.is_barrel:
            # For barrel layers we thin down the radius of the cylinder with dr = layer_width and r = rmin + (rmax - rmin)/2
            center_r = cyl.rmin + (cyl.rmax - cyl.rmin) * 0.5
            cyl.rmin = center_r - 0.5 * layer_width
            cyl.rmax = center_r + 0.5 * layer_width
        else:
            # For endcap layers we thin down the z thickness of the cylinder with dz = layer_width and z = zmin + (zmax - zmin)/2
            center_z = cyl.zmin + (cyl.zmax - cyl.zmin) * 0.5
            cyl.zmin = center_z - 0.5 * layer_width
            cyl.zmax = center_z + 0.5 * layer_width

        return cyl

    def plot_cell_vertices_rz(
        self,
        ax: None | plt.Axes = None,
        color: tuple[float, float, float] | str = "tab:blue",
        marker_size: float = 0.01,
        x_label: str = "z",
        y_label: str = "r",
    ) -> plt.Axes:
        """
        Plots the r-z coordinates of the cell vertices (edges) in the layer.

        Parameters:
        -----------
        ax : Union[None , plt.Axes], optional
            The matplotlib axes object to plot on, by default None.
        color : Union[tuple[float, float, float], str], optional
            The color of the markers, by default 'tab:blue'.
        marker_size : float, optional
            The size of the markers, by default 0.01.
        x_label : str, optional
            The label for the x-axis, by default 'z'.
        y_label : str, optional
            The label for the y-axis, by default 'r'.

        Returns:
        --------
        plt.Axes:
            The matplotlib axes object used for plotting.
        """
        if ax is None:
            fig = plt.figure()
            ax = fig.add_subplot()

        r_values, z_values = self._cell_vertices_rz(self.cells)

        ax.scatter(z_values, r_values, s=marker_size, color=color)

        ax.set_xlabel(x_label)
        ax.set_ylabel(y_label)

        return ax

    def plot_symmetrized_cylinder(
        self, cyl: Cylinder, ax: Axes3D = None, color: tuple[float, float, float] | str = "black"
    ) -> Axes3D:
        # If layer is continuous in z, plot as single cylinder
        if self.is_continuous_in_z():
            cyl_continuous = Cylinder(cyl.rmin, cyl.rmax, -cyl.zmax, cyl.zmax, cyl.is_barrel)
            plot_cylinder(cyl_continuous, ax=ax, color=color)
        # Otherwise, plot as two cylinders, one in each z halfspace
        else:
            cyl_pos_z_halfspace = Cylinder(cyl.rmin, cyl.rmax, cyl.zmin, cyl.zmax, cyl.is_barrel)
            cyl_neg_z_halfspace = Cylinder(cyl.rmin, cyl.rmax, -cyl.zmax, -cyl.zmin, cyl.is_barrel)
            plot_cylinder(cyl_pos_z_halfspace, ax=ax, color=color)
            plot_cylinder(cyl_neg_z_halfspace, ax=ax, color=color)

    def plot_thinned_cylinder(self, ax: Axes3D = None, color: tuple[float, float, float] | str = "red") -> Axes3D:
        """
        Plots the thinned version of the layer in 3D space.

        Parameters:
        -----------
        ax : Axes3D, optional
            The matplotlib 3D axes object to plot on, by default None.
        color : Union[tuple[float, float, float], str], optional
            The color of the cylinder, by default 'red'.

        Returns:
        --------
        Axes3D:
            The matplotlib 3D axes object used for plotting.
        """
        if ax is None:
            fig = plt.figure()
            ax = fig.add_subplot(111, projection="3d")

        cyl = self.get_thinned_cylinder()

        self.plot_symmetrized_cylinder(cyl, ax=ax, color=color)

        return ax

    def plot_cell_envelope(self, ax: Axes3D = None, color: tuple[float, float, float] | str = "red") -> Axes3D:
        """
        Plots the envelope of the cells in the layer in 3D space.

        Parameters:
        -----------
        ax : Axes3D, optional
            The matplotlib 3D axes object to plot on, by default None.
        color : Union[tuple[float, float, float], str], optional
            The color of the cylinder, by default 'red'.

        Returns:
        --------
        Axes3D:
            The matplotlib 3D axes object used for plotting.
        """
        if ax is None:
            fig = plt.figure()
            ax = fig.add_subplot(111, projection="3d")

        cyl = self.get_cell_envelope()

        self.plot_symmetrized_cylinder(cyl, ax=ax, color=color)

        return ax

    def plot(self, ax: Axes3D = None, thinned: bool = False, color: str = "red") -> Axes3D:
        """
        Plots the cells in the layer and either the cylinder envelope or the thinned down approximation in 3D space.

        Parameters:
        -----------
        ax : Axes3D, optional
            The matplotlib 3D axes object to plot on, by default None.
        thinned : bool, optional
            Whether to plot a thinned down version of the cells in the layer, by default False.
        color : str, optional
            The color of the cells, by default 'red'.

        Returns:
        --------
        Axes3D:
            The matplotlib 3D axes object used for plotting.
        """
        if ax is None:
            fig = plt.figure()
            ax = fig.add_subplot(111, projection="3d")

        # Plot the actual calorimeter cells
        plot_geometry(self.df, ax=ax, color=color)

        # Get either the envelope of the cells or the thinned down version of it
        cyl = self.get_thinned_cylinder() if thinned else self.get_cell_envelope()
        # plot the cylinder
        self.plot_symmetrized_cylinder(cyl, ax=ax)

        return ax

    def is_continuous_in_z(self, distance_threshold: float = 50) -> bool:
        """
        Checks whether the layer is continuous in z around z=0.
        Two cells with random phi are chosen that are closest to z=0 in the z>0 and z<0 halfspaces and their distance (edge to edge) is compared to a threshold.

        Parameters:
        -----------
        distance_threshold : float, optional
            The maximum distance between two consecutive cells in z for the layer to be considered continuous, by default 50.

        Returns:
        --------
        bool:
            True if the layer is continuous in z around z=0, False otherwise.
        """

        # Get (one of) the cells in the z>0 halfspace closest to z=0
        half_space_df = self.df[self.df.z > 0]
        min_z = half_space_df.z.min()
        pos_cell = half_space_df[half_space_df.z == min_z].iloc[0]
        # Get (one of) the cells in the z<0 halfspace closest to z=0
        half_space_df = self.df[self.df.z < 0]
        max_z = half_space_df.z.max()
        neg_cell = half_space_df[half_space_df.z == max_z].iloc[0]

        if self.coordinate_system in ["XYZ", "EtaPhiZ", "RPhiZ"]:
            dz_pos = pos_cell.dz
            dz_neg = neg_cell.dz
        elif self.coordinate_system == "EtaPhiR":
            # Estimate the dz with dz≈-Rsin(θ)dη (valid for small dη)
            theta_pos = 2 * np.arctan(np.exp(-pos_cell.eta))
            dz_pos = 2 * pos_cell.r * np.sin(theta_pos) * pos_cell.deta
            theta_neg = 2 * np.arctan(np.exp(-neg_cell.eta))
            dz_neg = 2 * neg_cell.r * np.sin(theta_neg) * neg_cell.deta

        min_z_pos_cell = pos_cell.z - dz_pos / 2
        max_z_neg_cell = neg_cell.z + dz_neg / 2

        if min_z_pos_cell < 0 or max_z_neg_cell > 0:
            # Cells in positive (negative) halfspace protrude into negative (positive) halfspace
            return True

        is_continuous = abs(min_z_pos_cell - max_z_neg_cell) < distance_threshold

        return bool(is_continuous)
