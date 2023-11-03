from __future__ import annotations

import numpy as np

from pygeosimplify.coordinate.definitions import XYZ, EtaPhiR, EtaPhiZ, RPhiZ
from pygeosimplify.geo.base import RectangularCell


class RPhiZCell(RectangularCell):
    """
    A class representing a rectangular cell in cylindrical coordinates (r, phi, z).
    """

    def __init__(self, dr: float, dphi: float, dz: float, pos: RPhiZ = RPhiZ(0, 0, 0)) -> None:  # noqa: B008
        """
        Initializes a new instance of the RPhiZCell class.

        Args:
        - dr (float): The length of the cell in the r direction.
        - dphi (float): The length of the cell in the phi direction.
        - dz (float): The length of the cell in the z direction.
        - pos (RPhiZ): The position of the cell in cylindrical coordinates (r, phi, z).

        Returns:
        - None
        """
        self.dr = dr
        self.dphi = dphi
        self.dz = dz
        self.pos = pos
        super().__init__(dr, dphi, dz, RPhiZ(pos.r, pos.phi, pos.z))
        # Convert all vertices to RPhiZ positions
        self.vertices = np.array([RPhiZ(vert[0], vert[1], vert[2]) for vert in self.vertices])

    @classmethod
    def create_from_vertices(cls, vertices: np.ndarray) -> RPhiZCell:
        """
        Creates a new instance of the RPhiZCell class from an array of vertices.

        Args:
        - vertices (np.ndarray): An array of vertices in cylindrical coordinates (r, phi, z).

        Returns:
        - RPhiZCell: A new instance of the RPhiZCell class.
        """
        if not all(isinstance(vert, RPhiZ) for vert in vertices):
            raise ValueError("Provided vertices for RPhiZ cell must be of type RPhiZ")
        obj = cls(0, 0, 0, RPhiZ(0, 0, 0))
        obj.vertices = vertices
        return obj


class XYZCell(RectangularCell):
    """
    A class representing a rectangular cell in 3D space with XYZ coordinates.
    """

    def __init__(self, dx: float, dy: float, dz: float, pos: XYZ = XYZ(0, 0, 0)) -> None:  # noqa: B008
        """
        Initializes a new instance of the XYZCell class.

        Args:
        - dx (float): The length of the cell along the x-axis.
        - dy (float): The length of the cell along the y-axis.
        - dz (float): The length of the cell along the z-axis.
        - pos (XYZ, optional): The position of the cell in 3D space. Defaults to XYZ(0, 0, 0).
        """
        self.dx = dx
        self.dy = dy
        self.dz = dz
        self.pos = pos
        super().__init__(dx, dy, dz, XYZ(pos.x, pos.y, pos.z))
        # Convert all vertices to XYZ positions
        self.vertices = np.array([XYZ(vert[0], vert[1], vert[2]) for vert in self.vertices])

    @classmethod
    def create_from_vertices(cls, vertices: np.ndarray) -> XYZCell:
        """
        Creates a new instance of the XYZCell class from an array of vertices.

        Args:
        - vertices (np.ndarray): An array of vertices representing the corners of the cell.

        Returns:
        - XYZCell: A new instance of the XYZCell class.
        """
        if not all(isinstance(vert, XYZ) for vert in vertices):
            raise ValueError("Provided vertices for XYZ cell must be of type XYZ")
        obj = cls(0, 0, 0, XYZ(0, 0, 0))
        obj.vertices = vertices
        return obj

    def to_RPhiZ(self) -> RPhiZCell:
        transformed_vertices = np.array([vert.to_RPhiZ() for vert in self.vertices])
        return RPhiZCell.create_from_vertices(vertices=transformed_vertices)


class EtaPhiRCell(RectangularCell):
    """
    A class representing a rectangular cell in the Eta-Phi-R coordinate system.

    Attributes:
    - deta (float): The size of the cell in the eta direction.
    - dphi (float): The size of the cell in the phi direction.
    - dr (float): The size of the cell in the r direction.
    - pos (EtaPhiR): The position of the cell in the Eta-Phi-R coordinate system.
    - vertices (np.ndarray): An array of EtaPhiR objects representing the vertices of the cell.

    Methods:
    - create_from_vertices(cls, vertices: np.ndarray) -> EtaPhiRCell: A class method that creates an EtaPhiRCell object from an array of vertices.
    """

    def __init__(self, deta: float, dphi: float, dr: float, pos: EtaPhiR = EtaPhiR(0, 0, 0)):  # noqa: B008
        self.deta = deta
        self.dphi = dphi
        self.dr = dr
        self.pos = pos
        super().__init__(deta, dphi, dr, EtaPhiR(pos.eta, pos.phi, pos.r))
        self.vertices = np.array([EtaPhiR(vert[0], vert[1], vert[2]) for vert in self.vertices])

    @classmethod
    def create_from_vertices(cls, vertices: np.ndarray) -> EtaPhiRCell:
        """
        A class method that creates an EtaPhiRCell object from an array of vertices.

        Args:
        - vertices (np.ndarray): An array of EtaPhiR objects representing the vertices of the cell.

        Returns:
        - EtaPhiRCell: An EtaPhiRCell object created from the provided vertices.
        """
        if not all(isinstance(vert, EtaPhiR) for vert in vertices):
            raise ValueError("Provided vertices for EtaPhiR cell must be of type EtaPhiR")
        obj = cls(0, 0, 0, EtaPhiR(0, 0, 0))
        obj.vertices = vertices
        return obj

    def to_XYZ(self) -> XYZCell:
        transformed_vertices = np.array([vert.to_XYZ() for vert in self.vertices])
        return XYZCell.create_from_vertices(vertices=transformed_vertices)

    def to_RPhiZ(self) -> RPhiZCell:
        transformed_vertices = np.array([vert.to_RPhiZ() for vert in self.vertices])
        return RPhiZCell.create_from_vertices(vertices=transformed_vertices)


class EtaPhiZCell(RectangularCell):
    """
    A class representing a rectangular cell in the Eta-Phi-Z coordinate system.
    """

    def __init__(self, deta: float, dphi: float, dz: float, pos: EtaPhiZ = EtaPhiZ(0, 0, 0)):  # noqa: B008
        """
        Initializes an instance of EtaPhiZCell.

        Args:
        - deta (float): The size of the cell in the eta direction.
        - dphi (float): The size of the cell in the phi direction.
        - dz (float): The size of the cell in the z direction.
        - pos (EtaPhiZ): The position of the cell in the Eta-Phi-Z coordinate system.
        - vertices (np.ndarray): An array of vertices that define the cell.
        """
        self.deta = deta
        self.dphi = dphi
        self.dz = dz
        self.pos = pos
        super().__init__(deta, dphi, dz, EtaPhiZ(pos.eta, pos.phi, pos.z))
        self.vertices = np.array([EtaPhiZ(vert[0], vert[1], vert[2]) for vert in self.vertices])

    @classmethod
    def create_from_vertices(cls, vertices: np.ndarray) -> EtaPhiZCell:
        """
        Creates an instance of EtaPhiZCell from an array of vertices.

        Args:
        - vertices (np.ndarray): An array of vertices that define the cell.

        Returns:
        - An instance of EtaPhiZCell.
        """
        if not all(isinstance(vert, EtaPhiZ) for vert in vertices):
            raise ValueError("Provided vertices for EtaPhiZ cell must be of type EtaPhiZ")
        obj = cls(0, 0, 0, EtaPhiZ(0, 0, 0))
        obj.vertices = vertices
        return obj

    def to_XYZ(self) -> XYZCell:
        transformed_vertices = np.array([vert.to_XYZ() for vert in self.vertices])
        return XYZCell.create_from_vertices(vertices=transformed_vertices)

    def to_RPhiZ(self) -> RPhiZCell:
        transformed_vertices = np.array([vert.to_RPhiZ() for vert in self.vertices])
        return RPhiZCell.create_from_vertices(vertices=transformed_vertices)
