import uproot


class FileHandler:
    def __init__(self, file_path: str, tree_name: str) -> None:
        self.file_path = file_path
        self.tree_name = tree_name
        self.file = self.read()

    def read(self) -> uproot.models.TTree:
        return uproot.open(f"{self.file_path}:{self.tree_name}")
