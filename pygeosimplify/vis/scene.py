import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from scipy.spatial import ConvexHull
from tqdm import tqdm

from pygeosimplify.geo.base import Cell


class CellScene:
    """
    A class for creating and plotting a scene of 3D cells.

    Attributes:
    -----------
    cell_list : List[Cell]
        A list of Cell objects to be plotted in the scene.

    Methods:
    --------
    add_cell(cell: Cell, facecolor: str = 'tab:orange', alpha: float = 0.1, edgecolor: tuple = (1, 1, 1, 1), edgewidth: float = 1) -> None
        Adds a Cell object to the cell_list with specified facecolor, alpha, edgecolor, and edgewidth.

    clear_cell_list() -> None
        Clears the cell_list.

    n_cells() -> int
        Returns the number of cells in the cell_list.

    min_max_cell_list_extent(dimIdx: int) -> tuple[float, float]
        Returns the minimum and maximum extent of the cell_list along the specified dimension.

    plot(ax: Axes3D = None, axisLabels: List[str] = []) -> Axes3D
        Plots the cells in the cell_list in a 3D plot with specified axis labels.
    """

    def __init__(self) -> None:
        self.cell_list: list[Cell] = []

    def add_cell(
        self,
        cell: Cell,
        facecolor: tuple[float, float, float] | str = "tab:orange",
        alpha: float = 0.1,
        edgecolor: tuple = (1, 1, 1, 1),
        edgewidth: float = 1,
    ) -> None:
        cell.facecolor = facecolor
        cell.alpha = alpha
        cell.edgecolor = edgecolor
        cell.edgewidth = edgewidth

        self.cell_list.append(cell)

    def clear_cell_list(self) -> None:
        self.cell_list = []

    def n_cells(self) -> int:
        return len(self.cell_list)

    def min_max_cell_list_extent(self, dimIdx: int) -> tuple[float, float]:
        extent = [cell.max_extent()[dimIdx] for cell in self.cell_list]
        min_extent = min([x[0] for x in extent])
        max_extent = max([x[1] for x in extent])
        return min_extent, max_extent

    def plot(
        self,
        ax: Axes3D = None,
        axis_limits: list[tuple[float, float]] | None = None,
        axis_labels: list[str] | None = None,
    ) -> Axes3D:
        if self.n_cells() == 0:
            raise RuntimeWarning("No cells to plot. Add cells using the add_cell method.")

        if ax is None:
            fig = plt.figure()
            ax = fig.add_subplot(111, projection="3d")

        ax.grid(False)
        ax.xaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
        ax.yaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
        ax.zaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))

        if axis_limits is None:
            min_max_x = self.min_max_cell_list_extent(0)
            min_max_y = self.min_max_cell_list_extent(1)
            min_max_z = self.min_max_cell_list_extent(2)
        else:
            min_max_x = axis_limits[0]
            min_max_y = axis_limits[1]
            min_max_z = axis_limits[2]

        ax.set_xlim(min_max_x)
        ax.set_ylim(min_max_y)
        ax.set_zlim(min_max_z)

        if axis_labels is not None:
            ax.set_xlabel(axis_labels[0])
            ax.set_ylabel(axis_labels[1])
            ax.set_zlabel(axis_labels[2])

        for cell in tqdm(self.cell_list):
            if type(cell.vertices[0]) is np.ndarray:
                raw_vertices = cell.vertices
            else:
                # Convert to raw vertices if cell coordinates are provided in specificy coordinate system
                raw_vertices = [(vert[0], vert[1], vert[2]) for vert in cell.vertices]
            # Compute convex hull of cell vertices
            hull = ConvexHull(raw_vertices)
            triangularFaces = hull.points[hull.simplices]

            ax.add_collection3d(
                Poly3DCollection(
                    triangularFaces,
                    facecolors=cell.facecolor,
                    linewidths=cell.edgewidth,
                    edgecolors=cell.edgecolor,
                    alpha=cell.alpha,
                )
            )

        return ax
