from pygeosimplify.utils.path_resolver import get_project_root

DATA_DIR = str(get_project_root()) + "/data/"

ATLAS_CALO_DATA_DIR = DATA_DIR + "ATLASCaloCells.root"

ATLAS_CALO_DATA_TREE_NAME = "caloDetCells"
