import pytest
from helpers import save_and_compare

import pygeosimplify as pgs
from pygeosimplify.cfg.test_data import CELL_ENERGY_DATA_DIR, CELL_ENERGY_DATA_TREE_NAME, REF_DIR


@pytest.fixture(name="atlas_cells_with_energy")
def test_load_geometry():
    pgs.set_coordinate_branch("XYZ", "isCartesian")
    pgs.set_coordinate_branch("EtaPhiR", "isCylindrical")
    pgs.set_coordinate_branch("EtaPhiZ", "isECCylindrical")

    df = pgs.load_geometry(CELL_ENERGY_DATA_DIR, CELL_ENERGY_DATA_TREE_NAME)

    # Test that energy branch is present and not empty or always 0
    assert "cell_energy" in df.columns
    assert not df["cell_energy"].empty
    assert not df["cell_energy"].eq(0).all()

    return df


def test_plot_cell_energy(atlas_cells_with_energy, tmpdir):
    pgs.plot_geometry(
        atlas_cells_with_energy,
        cell_energy_col="cell_energy",
        unit_scale=1e-3,
        unit_scale_energy=1e-3,
        axis_labels=["x [m]", "y [m]", "z [m]"],
        energy_label="Cell energy [GeV]",
        color_map="gist_heat_r",
    )

    assert save_and_compare("atlas_shower_cell_energy.png", REF_DIR, tmpdir, tol=0.5)
