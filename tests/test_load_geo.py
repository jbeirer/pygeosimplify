import pytest
import uproot

import pygeosimplify as pgs
from pygeosimplify.cfg.config import reset_coordinate_branches, set_coordinate_branch
from pygeosimplify.cfg.test_data import ATLAS_CALO_DATA_DIR, ATLAS_CALO_DATA_TREE_NAME


@pytest.fixture(name="atlas_calo_geo")
def test_load_geometry():
    reset_coordinate_branches()
    pgs.set_coordinate_branch("XYZ", "isXYZ")
    pgs.set_coordinate_branch("EtaPhiR", "isEtaPhiR")
    pgs.set_coordinate_branch("EtaPhiZ", "isEtaPhiZ")
    pgs.set_coordinate_branch("RPhiZ", "isRPhiZ")

    df = pgs.load_geometry(ATLAS_CALO_DATA_DIR, ATLAS_CALO_DATA_TREE_NAME)
    assert len(df.columns) == 19
    assert pgs.cfg.config.coordinate_branch_names["XYZ"] == "isXYZ"
    assert pgs.cfg.config.coordinate_branch_names["EtaPhiR"] == "isEtaPhiR"
    assert pgs.cfg.config.coordinate_branch_names["EtaPhiZ"] == "isEtaPhiZ"
    assert pgs.cfg.config.coordinate_branch_names["RPhiZ"] == "isRPhiZ"
    return df


def test_load_geometry_uproot():
    reset_coordinate_branches()
    tree = uproot.open(f"{ATLAS_CALO_DATA_DIR}:{ATLAS_CALO_DATA_TREE_NAME}")
    nKeys = len(tree.keys())
    assert nKeys == 19


def test_load_geometry_without_setting_coordinate_branch():
    reset_coordinate_branches()
    with pytest.raises(Exception):
        pgs.load_geometry(ATLAS_CALO_DATA_DIR, ATLAS_CALO_DATA_TREE_NAME)


def test_load_geometry_with_non_existing_coordinate_branch():
    reset_coordinate_branches()
    with pytest.raises(Exception):
        set_coordinate_branch("XYZ", "invalidBranch")
        pgs.load_geometry(ATLAS_CALO_DATA_DIR, ATLAS_CALO_DATA_TREE_NAME)
    reset_coordinate_branches()


def test_load_invalid_geometry(tmpdir):
    reset_coordinate_branches()
    # Create an empty file with only coordinate branches
    file = uproot.create(f"{tmpdir}/invalid_file.root")
    file.mktree("treeName", {"isXYZ": "int", "isEtaPhiR": "int", "isEtaPhiZ": "int"})

    # XYZ
    pgs.set_coordinate_branch("XYZ", "isXYZ")

    with pytest.raises(Exception):
        pgs.load_geometry(f"{tmpdir}/invalid_file.root", "treeName")

    assert {"x", "y", "z", "dx", "dy", "dz"} <= set(pgs.cfg.config.required_branches)
    reset_coordinate_branches()

    # EtaPhiR
    pgs.set_coordinate_branch("EtaPhiR", "isEtaPhiR")

    with pytest.raises(Exception):
        pgs.load_geometry(f"{tmpdir}/invalid_file.root", "treeName")

    assert {"eta", "phi", "r", "deta", "dphi", "dr"} <= set(pgs.cfg.config.required_branches)
    reset_coordinate_branches()

    # EtaPhiZ
    pgs.set_coordinate_branch("EtaPhiZ", "isEtaPhiZ")

    assert {"eta", "phi", "z", "deta", "dphi", "dz"} <= set(pgs.cfg.config.required_branches)
    reset_coordinate_branches()
