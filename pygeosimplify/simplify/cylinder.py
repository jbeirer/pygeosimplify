from dataclasses import dataclass, field


@dataclass
class Cylinder:
    rmin: float
    rmax: float
    zmin: float
    zmax: float
    is_barrel: bool


@dataclass
class CylinderGroup:
    envelope: dict[str, Cylinder] = field(default_factory=dict)
    thinned: dict[str, Cylinder] = field(default_factory=dict)
    processed: dict[str, Cylinder] = field(default_factory=dict)
