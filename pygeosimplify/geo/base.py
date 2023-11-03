from __future__ import annotations

from typing import Any

import numpy as np


class VertexSet:
    """
    A class representing a set of vertices.

    Attributes:
    -----------
    vertices : numpy.ndarray or None
        An array of shape (n, 2) representing the (x, y) coordinates of n vertices.
        If None, the set is empty.
    """

    def __init__(self, vertices: np.ndarray):
        self.vertices = vertices

    def __add__(self, other: VertexSet) -> VertexSet:
        """
        Returns a new VertexSet that is the union of the two VertexSets.

        Parameters:
        -----------
        other : VertexSet
            The other VertexSet to add.

        Returns:
        --------
        VertexSet
            A new VertexSet that is the union of the two VertexSets.
        """
        if self.vertices is None:
            return other
        elif other.vertices is None:
            return self
        else:
            return VertexSet(np.vstack((self.vertices, other.vertices)))


class Cuboid(VertexSet):
    """
    A class representing a cuboid in 3D space. For us a cuboid is simply a collection of vertices attached to a number of attributes.
    We assume that a cuboid is a convex polyhedra so that we can visualize the cuboid as convex hull of its vertices.

    Attributes:
    -----------
    facecolor : str
        The color of the cuboid's faces.
    alpha : float
        The transparency of the cuboid's faces.
    edgecolor : tuple
        The color of the cuboid's edges.
    edgewidth : int
        The width of the cuboid's edges.
    """

    def __init__(
        self,
        vertices: np.ndarray,
        facecolor: str = "tab:orange",
        alpha: float = 0.1,
        edgecolor: tuple = (1, 1, 1, 1),
        edgewidth: float = 1,
    ):
        super().__init__(vertices)

    def max_extent_in_dim(self, dimIdx: int) -> list:
        """
        Returns the minimum and maximum values of the cuboid's vertices in the specified dimension.

        Parameters:
        -----------
        dimIdx : int
            The index of the dimension to compute the extent for.

        Returns:
        --------
        list
            A list containing the minimum and maximum values of the cuboid's vertices in the specified dimension.
        """
        values = [vertex[dimIdx] for vertex in self.vertices]
        return [min(values), max(values)]

    def max_extent(self) -> tuple:
        """
        Returns the minimum and maximum values of the cuboid's vertices in all three dimensions.

        Returns:
        --------
        tuple
            A tuple containing three lists, each containing the minimum and maximum values of the cuboid's vertices
            in one of the three dimensions.
        """
        return self.max_extent_in_dim(0), self.max_extent_in_dim(1), self.max_extent_in_dim(2)


class RectangularCuboid(Cuboid):
    """
    A class representing a rectangular cuboid defined by its dimensions and center position.
    No implicit coordinate system is assumed at this point.

    Args:
        di (float): The length of the cuboid along the x-axis.
        dj (float): The length of the cuboid along the y-axis.
        dk (float): The length of the cuboid along the z-axis.
        pos (XYZ, optional): The center position of the cuboid. Defaults to XYZ(0,0,0).
    """

    def __init__(self, di: float, dj: float, dk: float, pos: Any):
        self.di = di
        self.dj = dj
        self.dk = dk
        self.pos = pos
        self.set_vertices()
        self.has_coordinate_system = False

    def set_vertices(self) -> None:
        # Calculate half dimensions
        half_di = self.di / 2
        half_dj = self.dj / 2
        half_dk = self.dk / 2

        # Define the eight vertices of the cuboid with the specified center position
        self.vertices = np.array(
            [
                [self.pos[0] - half_di, self.pos[1] - half_dj, self.pos[2] - half_dk],
                [self.pos[0] + half_di, self.pos[1] - half_dj, self.pos[2] - half_dk],
                [self.pos[0] + half_di, self.pos[1] + half_dj, self.pos[2] - half_dk],
                [self.pos[0] - half_di, self.pos[1] + half_dj, self.pos[2] - half_dk],
                [self.pos[0] - half_di, self.pos[1] - half_dj, self.pos[2] + half_dk],
                [self.pos[0] + half_di, self.pos[1] - half_dj, self.pos[2] + half_dk],
                [self.pos[0] + half_di, self.pos[1] + half_dj, self.pos[2] + half_dk],
                [self.pos[0] - half_di, self.pos[1] + half_dj, self.pos[2] + half_dk],
            ]
        )
