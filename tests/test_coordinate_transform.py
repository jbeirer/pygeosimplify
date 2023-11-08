import pytest

from pygeosimplify.cfg.config import coordinate_branch_names, set_coordinate_branch, set_coordinate_branch_dict
from pygeosimplify.coordinate.definitions import XYZ, EtaPhiR, EtaPhiZ


def test_set_coordinate_branch():
    # Test setting a coordinate branch for a valid coordinate system
    set_coordinate_branch("XYZ", "isCartesian")
    set_coordinate_branch("EtaPhiR", "isCylindrical")
    set_coordinate_branch("EtaPhiZ", "isECCylindrical")
    assert coordinate_branch_names["XYZ"] == "isCartesian"
    assert coordinate_branch_names["EtaPhiR"] == "isCylindrical"
    assert coordinate_branch_names["EtaPhiZ"] == "isECCylindrical"

    # Test setting coordinate branch via dict
    set_coordinate_branch_dict({"XYZ": "isCartesian", "EtaPhiR": "isCylindrical", "EtaPhiZ": "isECCylindrical"})
    assert coordinate_branch_names["XYZ"] == "isCartesian"
    assert coordinate_branch_names["EtaPhiR"] == "isCylindrical"
    assert coordinate_branch_names["EtaPhiZ"] == "isECCylindrical"

    # Test setting a unsupported coordinate system
    with pytest.raises(ValueError):
        set_coordinate_branch("invalidCoordinateSystem", "isCartesian")

    # Test setting unsupported coordinate system with dict
    with pytest.raises(ValueError):
        set_coordinate_branch_dict({"invalidCoordinateSystem": "isCartesian"})


def test_XYZ_to_RPhiZ():
    xyz = XYZ(1, 2, 3)
    rphiz = xyz.to_RPhiZ()

    assert pytest.approx(rphiz.r, abs=1e-7) == 2.23606798
    assert pytest.approx(rphiz.phi, abs=1e-7) == 1.10714872
    assert pytest.approx(rphiz.z, abs=1e-7) == 3


def test_EtaPhiR_to_RPhiZ():
    etaphir = EtaPhiR(1, 2, 3)
    rphiz = etaphir.to_RPhiZ()

    assert pytest.approx(rphiz.r, abs=1e-7) == 3
    assert pytest.approx(rphiz.phi, abs=1e-7) == 2
    assert pytest.approx(rphiz.z, abs=1e-7) == 3.52560358


def test_EtaPhiR_to_XYZ():
    etaphir = EtaPhiR(1, 2, 3)
    xyz = etaphir.to_XYZ()

    assert pytest.approx(xyz.x, abs=1e-7) == -1.24844051
    assert pytest.approx(xyz.y, abs=1e-7) == 2.72789228
    assert pytest.approx(xyz.z, abs=1e-7) == 3.52560358


def test_EtaPhiZ_to_XYZ():
    etaphiz = EtaPhiZ(1, 2, 3)
    xyz = etaphiz.to_XYZ()

    assert pytest.approx(xyz.x, abs=1e-7) == -1.06232066
    assert pytest.approx(xyz.y, abs=1e-7) == 2.32121299
    assert pytest.approx(xyz.z, abs=1e-7) == 3


def test_EtaPhiZ_to_RPhiZ():
    etaphiz = EtaPhiZ(1, 2, 3)
    rphiz = etaphiz.to_RPhiZ()

    assert pytest.approx(rphiz.r, abs=1e-7) == 2.55275438
    assert pytest.approx(rphiz.phi, abs=1e-7) == 2
    assert pytest.approx(rphiz.z, abs=1e-7) == 3
