from dataclasses import dataclass

import numpy as np


@dataclass
class RPhiZ:
    r: float
    phi: float
    z: float


@dataclass
class XYZ:
    x: float
    y: float
    z: float

    def to_RPhiZ(self) -> RPhiZ:
        r = np.sqrt(self.x**2 + self.y**2)
        phi = np.arctan2(self.y, self.x)
        z = self.z

        return RPhiZ(r, phi, z)


@dataclass
class EtaPhiR:
    eta: float
    phi: float
    r: float

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
