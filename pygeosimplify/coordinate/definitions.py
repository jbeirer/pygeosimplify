from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np


@dataclass
class RPhiZ:
    r: float
    phi: float
    z: float

    def __getitem__(self, idx: int) -> float:
        return [self.r, self.phi, self.z][idx]

    def __add__(self, other: RPhiZ) -> RPhiZ:
        if isinstance(other, RPhiZ):
            return RPhiZ(self.r + other.r, self.phi + other.phi, self.z + other.z)
        else:
            raise TypeError("Unsupported operand type for +")

    def __sub__(self, other: RPhiZ) -> RPhiZ:
        if isinstance(other, RPhiZ):
            return RPhiZ(self.r - other.r, self.phi - other.phi, self.z - other.z)
        else:
            raise TypeError("Unsupported operand type for -")

    def __abs__(self) -> float:
        return math.sqrt(self.r**2 + self.phi**2 + self.z**2)

    def to_EtaPhiR(self) -> EtaPhiR:
        r = self.r
        theta = np.arctan2(r, self.z)
        eta = -np.log(np.tan(theta / 2)) if theta != 0 else 0
        phi = self.phi

        return EtaPhiR(eta, phi, r)

    def to_EtaPhiZ(self) -> EtaPhiZ:
        theta = np.arctan2(self.r, self.z)
        eta = -np.log(np.tan(theta / 2)) if theta != 0 else 0
        phi = self.phi
        z = self.z
        return EtaPhiZ(eta, phi, z)

    def to_XYZ(self) -> XYZ:
        x = self.r * np.cos(self.phi)
        y = self.r * np.sin(self.phi)
        z = self.z

        return XYZ(x, y, z)


@dataclass
class XYZ:
    x: float
    y: float
    z: float

    def __getitem__(self, idx: int) -> float:
        return [self.x, self.y, self.z][idx]

    def __add__(self, other: XYZ) -> XYZ:
        if isinstance(other, XYZ):
            return XYZ(self.x + other.x, self.y + other.y, self.z + other.z)
        else:
            raise TypeError("Unsupported operand type for +")

    def __sub__(self, other: XYZ) -> XYZ:
        if isinstance(other, XYZ):
            return XYZ(self.x - other.x, self.y - other.y, self.z - other.z)
        else:
            raise TypeError("Unsupported operand type for -")

    def __abs__(self) -> float:
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)

    def to_RPhiZ(self) -> RPhiZ:
        r = np.sqrt(self.x**2 + self.y**2)
        phi = np.arctan2(self.y, self.x)
        z = self.z

        return RPhiZ(r, phi, z)

    def to_EtaPhiR(self) -> EtaPhiR:
        r = np.sqrt(self.x**2 + self.y**2)
        theta = np.arctan2(r, self.z)
        eta = -np.log(np.tan(theta / 2)) if theta != 0 else 0
        phi = np.arctan2(self.y, self.x)

        return EtaPhiR(eta, phi, r)

    def to_EtaPhiZ(self) -> EtaPhiZ:
        theta = np.arctan2(np.sqrt(self.x**2 + self.y**2), self.z)
        eta = -np.log(np.tan(theta / 2)) if theta != 0 else 0
        phi = np.arctan2(self.y, self.x)
        z = self.z

        return EtaPhiZ(eta, phi, z)


@dataclass
class EtaPhiR:
    eta: float
    phi: float
    r: float

    def __getitem__(self, idx: int) -> float:
        return [self.eta, self.phi, self.r][idx]

    def __add__(self, other: EtaPhiR) -> EtaPhiR:
        if isinstance(other, EtaPhiR):
            return EtaPhiR(self.eta + other.eta, self.phi + other.phi, self.r + other.r)
        else:
            raise TypeError("Unsupported operand type for +")

    def __sub__(self, other: EtaPhiR) -> EtaPhiR:
        if isinstance(other, EtaPhiR):
            return EtaPhiR(self.eta - other.eta, self.phi - other.phi, self.r - other.r)
        else:
            raise TypeError("Unsupported operand type for -")

    def __abs__(self) -> float:
        return math.sqrt(self.eta**2 + self.phi**2 + self.r**2)

    def to_RPhiZ(self) -> RPhiZ:
        r = self.r
        phi = self.phi
        z = r * np.sinh(self.eta)

        return RPhiZ(r, phi, z)

    def to_XYZ(self) -> XYZ:
        x = self.r * np.cos(self.phi)
        y = self.r * np.sin(self.phi)
        z = self.r * np.sinh(self.eta)

        return XYZ(x, y, z)


@dataclass
class EtaPhiZ:
    eta: float
    phi: float
    z: float

    def __getitem__(self, idx: int) -> float:
        return [self.eta, self.phi, self.z][idx]

    def __add__(self, other: EtaPhiZ) -> EtaPhiZ:
        if isinstance(other, EtaPhiZ):
            return EtaPhiZ(self.eta + other.eta, self.phi + other.phi, self.z + other.z)
        else:
            raise TypeError("Unsupported operand type for +")

    def __sub__(self, other: EtaPhiZ) -> EtaPhiZ:
        if isinstance(other, EtaPhiZ):
            return EtaPhiZ(self.eta - other.eta, self.phi - other.phi, self.z - other.z)
        else:
            raise TypeError("Unsupported operand type for -")

    def __abs__(self) -> float:
        return math.sqrt(self.eta**2 + self.phi**2 + self.z**2)

    def to_XYZ(self) -> XYZ:
        r = self.z / np.sinh(self.eta)
        x = r * np.cos(self.phi)
        y = r * np.sin(self.phi)
        z = self.z

        return XYZ(x, y, z)

    def to_RPhiZ(self) -> RPhiZ:
        r = self.z / np.sinh(self.eta)
        phi = self.phi
        z = self.z

        return RPhiZ(r, phi, z)
