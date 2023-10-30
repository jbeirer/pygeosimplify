from pygeosimplify.io import file_handler
from pygeosimplify.utils.path_resolver import get_project_root


def test_file_read():
    projectRootPath = get_project_root()
    inputPath = f"{projectRootPath}/data/ATLASCaloCells.root"

    fh = file_handler.FileHandler(inputPath, "caloDetCells")

    keys = fh.file.keys()
    nKeys = len(keys)

    assert nKeys == 19
