import pandas as pd
import uproot


def load_geometry(file_path: str, tree_name: str) -> pd.DataFrame:
    geoTTree = uproot.open(f"{file_path}:{tree_name}")

    geoDF = uprootTreeToDataFrame(geoTTree)

    return geoDF


def uprootTreeToDataFrame(tree: uproot.models.TTree) -> pd.DataFrame:
    df = tree.arrays(tree.keys(), library="pd")

    return df
