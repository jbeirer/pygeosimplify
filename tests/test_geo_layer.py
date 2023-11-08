import matplotlib.pyplot as plt
import pytest
from matplotlib.testing.compare import compare_images
from test_load_geo import test_load_geometry as atlas_calo_geo  # noqa: F401

from pygeosimplify.cfg.test_data import REF_DIR
from pygeosimplify.simplify.layer import GeoLayer


def test_geo_endcap_layer(atlas_calo_geo, tmpdir):  # noqa: F811
    layer = GeoLayer(atlas_calo_geo, layer_idx=23)

    assert layer.idx == 23
    assert layer.coordinate_system == "XYZ"
    assert layer.is_barrel is False
    assert pytest.approx(layer.extent["rmin"]) == 84.09978870164535
    assert pytest.approx(layer.extent["rmax"]) == 458.8423527799789
    assert pytest.approx(layer.extent["zmin"]) == -5979.525192260742
    assert pytest.approx(layer.extent["zmax"]) == 5979.525192260742

    # Plot layer and envelope in 3D
    layer.plot(thinned=False)
    plt.savefig(f"{tmpdir}/test.png", dpi=300)
    assert compare_images(f"{REF_DIR}/ATLAS_endcap_layer23_validation.png", f"{tmpdir}/test.png", tol=0.5) is None

    # Plots the r-z positions of the cell vertices in the layer
    layer.plot_cell_vertices_rz()
    plt.savefig(f"{tmpdir}/test.png", dpi=300)
    assert compare_images(f"{REF_DIR}/ATLAS_endcap_layer23_cell_vertices_rz.png", f"{tmpdir}/test.png", tol=0.5) is None


def test_geo_barrel_layer(atlas_calo_geo, tmpdir):  # noqa: F811
    layer = GeoLayer(atlas_calo_geo, layer_idx=18)

    assert layer.idx == 18
    assert layer.coordinate_system == "EtaPhiR"
    assert layer.is_barrel is True
    assert pytest.approx(layer.extent["rmin"]) == 2300.0
    assert pytest.approx(layer.extent["rmax"]) == 2600.0
    assert pytest.approx(layer.extent["zmin"]) == -6209.913044250297
    assert pytest.approx(layer.extent["zmax"]) == 6221.093028802642

    # Plot layer and envelope in 3D
    layer.plot(thinned=False)
    plt.savefig(f"{tmpdir}/test.png", dpi=300)
    assert compare_images(f"{REF_DIR}/ATLAS_barrel_layer18_validation.png", f"{tmpdir}/test.png", tol=0.5) is None

    # Plots the r-z positions of the cell vertices in the layer
    layer.plot_cell_vertices_rz()
    plt.savefig(f"{tmpdir}/test.png", dpi=300)
    assert compare_images(f"{REF_DIR}/ATLAS_barrel_layer18_cell_vertices_rz.png", f"{tmpdir}/test.png", tol=0.5) is None
