import pytest
import uproot

import pygeosimplify as pgs
from pygeosimplify.cfg.config import set_coordinate_branch, set_coordinate_branch_dict
from pygeosimplify.cfg.test_data import ATLAS_CALO_DATA_DIR, ATLAS_CALO_DATA_TREE_NAME
from pygeosimplify.io.geo_handler import tree_to_df


@pytest.fixture
def loaded_geometry_uproot():
    tree = uproot.open(f"{ATLAS_CALO_DATA_DIR}:{ATLAS_CALO_DATA_TREE_NAME}")
    df = tree_to_df(tree)
    return df


def test_load_geometry_uproot(loaded_geometry_uproot):
    nKeys = len(loaded_geometry_uproot.keys())
    assert nKeys == 18


def test_load_geometry():
    pgs.set_coordinate_branch("XYZ", "isCartesian")
    pgs.set_coordinate_branch("EtaPhiR", "isCylindrical")
    pgs.set_coordinate_branch("EtaPhiZ", "isECCylindrical")

    df = pgs.load_geometry(ATLAS_CALO_DATA_DIR, ATLAS_CALO_DATA_TREE_NAME)
    assert len(df.columns) == 18


def test_load_geometry_without_setting_coordinate_branch():
    set_coordinate_branch_dict({})
    with pytest.raises(Exception):
        pgs.load_geometry(ATLAS_CALO_DATA_DIR, ATLAS_CALO_DATA_TREE_NAME)


def test_load_geometry_with_non_existing_coordinate_branch():
    with pytest.raises(Exception):
        set_coordinate_branch("XYZ", "invalidBranch")
        pgs.load_geometry(ATLAS_CALO_DATA_DIR, ATLAS_CALO_DATA_TREE_NAME)
