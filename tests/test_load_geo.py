import pytest
import uproot

import pygeosimplify as pgs
from pygeosimplify.cfg.config import reset_coordinate_branches, set_coordinate_branch
from pygeosimplify.cfg.test_data import ATLAS_CALO_DATA_DIR, ATLAS_CALO_DATA_TREE_NAME


def test_load_geometry_uproot():
    tree = uproot.open(f"{ATLAS_CALO_DATA_DIR}:{ATLAS_CALO_DATA_TREE_NAME}")
    nKeys = len(tree.keys())
    assert nKeys == 18


def test_load_geometry_without_setting_coordinate_branch():
    with pytest.raises(Exception):
        pgs.load_geometry(ATLAS_CALO_DATA_DIR, ATLAS_CALO_DATA_TREE_NAME)


def test_load_geometry_with_non_existing_coordinate_branch():
    with pytest.raises(Exception):
        set_coordinate_branch("XYZ", "invalidBranch")
        pgs.load_geometry(ATLAS_CALO_DATA_DIR, ATLAS_CALO_DATA_TREE_NAME)
    reset_coordinate_branches()


def test_load_invalid_geometry(tmpdir):
    # Create an empty file with only coordinate branches
    file = uproot.create(f"{tmpdir}/invalid_file.root")
    file.mktree("treeName", {"isCartesian": "int", "isCylindrical": "int", "isECCylindrical": "int"})

    # XYZ
    pgs.set_coordinate_branch("XYZ", "isCartesian")

    with pytest.raises(Exception):
        pgs.load_geometry(f"{tmpdir}/invalid_file.root", "treeName")

    assert {"x", "y", "z", "dx", "dy", "dz"} <= set(pgs.cfg.config.required_branches)
    reset_coordinate_branches()

    # EtaPhiR
    pgs.set_coordinate_branch("EtaPhiR", "isCylindrical")

    with pytest.raises(Exception):
        pgs.load_geometry(f"{tmpdir}/invalid_file.root", "treeName")

    assert {"eta", "phi", "r", "deta", "dphi", "dr"} <= set(pgs.cfg.config.required_branches)
    reset_coordinate_branches()

    # EtaPhiZ
    pgs.set_coordinate_branch("EtaPhiZ", "isECCylindrical")

    assert {"eta", "phi", "z", "deta", "dphi", "dz"} <= set(pgs.cfg.config.required_branches)
    reset_coordinate_branches()


@pytest.fixture(name="atlas_calo_geo")
def test_load_geometry():
    pgs.set_coordinate_branch("XYZ", "isCartesian")
    pgs.set_coordinate_branch("EtaPhiR", "isCylindrical")
    pgs.set_coordinate_branch("EtaPhiZ", "isECCylindrical")

    df = pgs.load_geometry(ATLAS_CALO_DATA_DIR, ATLAS_CALO_DATA_TREE_NAME)
    assert len(df.columns) == 18
    assert pgs.cfg.config.coordinate_branch_names["XYZ"] == "isCartesian"
    assert pgs.cfg.config.coordinate_branch_names["EtaPhiR"] == "isCylindrical"
    assert pgs.cfg.config.coordinate_branch_names["EtaPhiZ"] == "isECCylindrical"
    return df
