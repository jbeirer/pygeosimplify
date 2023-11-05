import pytest
import uproot

import pygeosimplify as pgs
from pygeosimplify.cfg.config import set_coordinate_branch, set_coordinate_branch_dict
from pygeosimplify.cfg.test_data import ATLAS_CALO_DATA_DIR, ATLAS_CALO_DATA_TREE_NAME


def test_load_geometry_uproot():
    tree = uproot.open(f"{ATLAS_CALO_DATA_DIR}:{ATLAS_CALO_DATA_TREE_NAME}")
    nKeys = len(tree.keys())
    assert nKeys == 18


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


def test_load_geometry_without_setting_coordinate_branch():
    set_coordinate_branch_dict({})
    with pytest.raises(Exception):
        pgs.load_geometry(ATLAS_CALO_DATA_DIR, ATLAS_CALO_DATA_TREE_NAME)


def test_load_geometry_with_non_existing_coordinate_branch():
    with pytest.raises(Exception):
        set_coordinate_branch("XYZ", "invalidBranch")
        pgs.load_geometry(ATLAS_CALO_DATA_DIR, ATLAS_CALO_DATA_TREE_NAME)


def test_load_invalid_geometry(tmpdir):
    # Create an empty file with only coordinate branches
    file = uproot.create(f"{tmpdir}/invalid_file.root")
    file.mktree("treeName", {"isCartesian": "int", "isCylindrical": "int", "isECCylindrical": "int"})

    pgs.set_coordinate_branch("XYZ", "isCartesian")
    pgs.set_coordinate_branch("EtaPhiR", "isCylindrical")
    pgs.set_coordinate_branch("EtaPhiZ", "isECCylindrical")

    with pytest.raises(Exception):
        pgs.load_geometry("invalid_file.root", "treeName")
