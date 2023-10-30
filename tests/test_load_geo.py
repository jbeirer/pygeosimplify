import uproot

import pygeosimplify as pgs
from pygeosimplify.io.geo_handler import uprootTreeToDataFrame
from pygeosimplify.utils.path_resolver import get_project_root


def test_load_geometry_uproot():
    projectRootPath = get_project_root()
    inputPath = f"{projectRootPath}/data/ATLASCaloCells.root"

    geoTTree = uproot.open(f"{inputPath}:caloDetCells")

    geoDF = uprootTreeToDataFrame(geoTTree)

    keys = geoDF.keys()
    nKeys = len(keys)

    assert nKeys == 19


def test_load_geometry():
    projectRootPath = get_project_root()
    inputPath = f"{projectRootPath}/data/ATLASCaloCells.root"

    geoDf = pgs.load_geometry(inputPath, "caloDetCells")

    assert len(geoDf.columns) == 19
