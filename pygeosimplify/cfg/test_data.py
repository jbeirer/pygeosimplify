from pygeosimplify.utils.path_resolver import get_project_root

DATA_DIR = str(get_project_root()) + "/tests/data/"
REF_DIR = str(get_project_root()) + "/tests/refs/"

# Data for ATLAS calorimeter cells
ATLAS_CALO_DATA_DIR = DATA_DIR + "ATLASCaloCells.root"
ATLAS_CALO_DATA_TREE_NAME = "caloDetCells"

# Data of ATLAS calorimeter cells with simulated energy from photon shower
CELL_ENERGY_DATA_DIR = DATA_DIR + "cell_energy_data.root"
CELL_ENERGY_DATA_TREE_NAME = "caloDetCells"
