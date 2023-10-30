import uproot

import pygeosimplify as pgs
from pygeosimplify.cfg.test_data import ATLAS_CALO_DATA_DIR, ATLAS_CALO_DATA_TREE_NAME
from pygeosimplify.io.geo_handler import tree_to_df


def test_load_geometry_uproot():
    tree = uproot.open(f"{ATLAS_CALO_DATA_DIR}:{ATLAS_CALO_DATA_TREE_NAME}")

    df = tree_to_df(tree)

    keys = df.keys()
    nKeys = len(keys)

    assert nKeys == 18


def test_load_geometry():
    pgs.set_coordinate_branch("XYZ", "isCartesian")
    pgs.set_coordinate_branch("EtaPhiR", "isCylindrical")
    pgs.set_coordinate_branch("EtaPhiZ", "isECCylindrical")

    df = pgs.load_geometry(ATLAS_CALO_DATA_DIR, ATLAS_CALO_DATA_TREE_NAME)

    assert len(df.columns) == 18
