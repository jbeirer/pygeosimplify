import pytest

from pygeosimplify.cfg.config import coordinate_branch_names, set_coordinate_branch
from pygeosimplify.cfg.test_data import ATLAS_CALO_DATA_DIR, ATLAS_CALO_DATA_TREE_NAME
from pygeosimplify.coordinate.definitions import XYZ, EtaPhiR, EtaPhiZ
from pygeosimplify.io.geo_handler import load_geometry


def test_set_coordinate_branch():
    # Test setting a coordinate branch for a valid coordinate system
    set_coordinate_branch("XYZ", "isCartesian")
    assert coordinate_branch_names["XYZ"] == "isCartesian"

    # Test setting a unsupported coordinate system
    with pytest.raises(ValueError):
        set_coordinate_branch("invalidCoordinateSystem", "isCartesian")

    # Test setting a coordinate branch that does not exist
    with pytest.raises(Exception):
        set_coordinate_branch("XYZ", "invalidBranch")
        load_geometry(ATLAS_CALO_DATA_DIR, ATLAS_CALO_DATA_TREE_NAME)


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
