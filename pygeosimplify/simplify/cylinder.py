from dataclasses import dataclass, field


@dataclass
class Cylinder:
    rmin: float
    rmax: float
    zmin: float
    zmax: float
    is_barrel: bool

    def __post_init__(self) -> None:
        # Initialize a dictionary to keep track of the lock status of each attribute
        # Note that the lock is just an attribute and does not actually prevent the value from being changed
        self._locks = {"rmin": False, "rmax": False, "zmin": False, "zmax": False, "is_barrel": False}

    def lock(self, attr: str) -> None:
        if attr in self._locks:
            self._locks[attr] = True
        else:
            raise AttributeError(f"No such attribute: {attr}")

    def unlock(self, attr: str) -> None:
        if attr in self._locks:
            self._locks[attr] = False
        else:
            raise AttributeError(f"No such attribute: {attr}")

    def is_locked(self, attr: str) -> bool:
        if attr in self._locks:
            return self._locks[attr]
        else:
            raise AttributeError(f"No such attribute: {attr}")


@dataclass
class CylinderGroup:
    envelope: dict[str, Cylinder] = field(default_factory=dict)
    thinned: dict[str, Cylinder] = field(default_factory=dict)
    processed: dict[str, Cylinder] = field(default_factory=dict)
