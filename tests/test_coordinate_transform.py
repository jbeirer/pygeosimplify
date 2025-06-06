import pytest

from pygeosimplify.cfg.config import coordinate_branch_names, set_coordinate_branch, set_coordinate_branch_dict
from pygeosimplify.coordinate.definitions import XYZ, EtaPhiR, EtaPhiZ, RPhiZ


def test_set_coordinate_branch():
    # Test setting a coordinate branch for a valid coordinate system
    set_coordinate_branch("XYZ", "isXYZ")
    set_coordinate_branch("EtaPhiR", "isEtaPhiR")
    set_coordinate_branch("EtaPhiZ", "isEtaPhiZ")
    set_coordinate_branch("RPhiZ", "isRPhiZ")
    assert coordinate_branch_names["XYZ"] == "isXYZ"
    assert coordinate_branch_names["EtaPhiR"] == "isEtaPhiR"
    assert coordinate_branch_names["EtaPhiZ"] == "isEtaPhiZ"
    assert coordinate_branch_names["RPhiZ"] == "isRPhiZ"

    # Test setting coordinate branch via dict
    set_coordinate_branch_dict(
        {
            "XYZ": "isXYZ",
            "EtaPhiR": "isEtaPhiR",
            "EtaPhiZ": "isEtaPhiZ",
            "RPhiZ": "isRPhiZ",
        }
    )
    assert coordinate_branch_names["XYZ"] == "isXYZ"
    assert coordinate_branch_names["EtaPhiR"] == "isEtaPhiR"
    assert coordinate_branch_names["EtaPhiZ"] == "isEtaPhiZ"
    assert coordinate_branch_names["RPhiZ"] == "isRPhiZ"

    # Test setting a unsupported coordinate system
    with pytest.raises(ValueError):
        set_coordinate_branch("invalidCoordinateSystem", "isXYZ")

    # Test setting unsupported coordinate system with dict
    with pytest.raises(ValueError):
        set_coordinate_branch_dict({"invalidCoordinateSystem": "isXYZ"})


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


def test_RPhiZ_to_XYZ():
    rphiz = RPhiZ(1, 2, 3)
    xyz = rphiz.to_XYZ()

    assert pytest.approx(xyz.x, abs=1e-7) == -0.4161468
    assert pytest.approx(xyz.y, abs=1e-7) == 0.90929742
    assert pytest.approx(xyz.z, abs=1e-7) == 3


def test_RPhiZ_to_EtaPhiZ():
    rphiz = RPhiZ(1, 2, 3)
    etaphiz = rphiz.to_EtaPhiZ()

    assert pytest.approx(etaphiz.eta, abs=1e-7) == 1.81844645
    assert pytest.approx(etaphiz.phi, abs=1e-7) == 2
    assert pytest.approx(etaphiz.z, abs=1e-7) == 3


def test_RPhiZ_to_EtaPhiR():
    rphiz = RPhiZ(1, 2, 3)
    etaphir = rphiz.to_EtaPhiR()

    assert pytest.approx(etaphir.eta, abs=1e-7) == 1.81844645
    assert pytest.approx(etaphir.phi, abs=1e-7) == 2
    assert pytest.approx(etaphir.r, abs=1e-7) == 1
