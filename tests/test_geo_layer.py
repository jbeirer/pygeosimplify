import pytest
from helpers import save_and_compare
from test_load_geo import test_load_geometry as atlas_calo_geo  # noqa: F401

from pygeosimplify.cfg.test_data import REF_DIR
from pygeosimplify.simplify.layer import GeoLayer


def test_geo_barrel_layer_14(atlas_calo_geo, tmpdir):  # noqa: F811
    layer = GeoLayer(atlas_calo_geo, layer_idx=14)

    assert layer.idx == "14"
    assert layer.coordinate_system == "EtaPhiR"
    assert bool(layer.is_barrel) is True
    assert pytest.approx(layer.extent["rmin"]) == 3440
    assert pytest.approx(layer.extent["rmax"]) == 3820
    assert pytest.approx(layer.extent["zmin"]) == -2897.78986248739
    assert pytest.approx(layer.extent["zmax"]) == 2897.78986248739

    # Plot layer and envelope in 3D
    layer.plot(thinned=False)
    assert save_and_compare("ATLAS_barrel_layer14_validation.png", REF_DIR, tmpdir, tol=0.5)

    # Plots the r-z positions of the cell vertices in the layer
    layer.plot_cell_vertices_rz()
    assert save_and_compare("ATLAS_barrel_layer14_cell_vertices_rz.png", REF_DIR, tmpdir, tol=0.5)

    # The thinned down cylinder with infinitesimal dr
    thinned_cyl = layer.get_thinned_cylinder()

    assert pytest.approx(thinned_cyl.rmin) == 3625.0
    assert pytest.approx(thinned_cyl.rmax) == 3635.0
    assert pytest.approx(thinned_cyl.zmin) == 344.5736252199143
    assert pytest.approx(thinned_cyl.zmax) == 2897.78986248739


def test_geo_barrel_layer_18(atlas_calo_geo, tmpdir):  # noqa: F811
    layer = GeoLayer(atlas_calo_geo, layer_idx=18)

    assert layer.idx == "18"
    assert layer.coordinate_system == "EtaPhiR"
    assert bool(layer.is_barrel) is True
    assert pytest.approx(layer.extent["rmin"]) == 2300.0
    assert pytest.approx(layer.extent["rmax"]) == 2600.0
    assert pytest.approx(layer.extent["zmin"]) == -6209.913044250297
    assert pytest.approx(layer.extent["zmax"]) == 6221.093028802642

    # Plot layer and envelope in 3D
    layer.plot(thinned=False)
    assert save_and_compare("ATLAS_barrel_layer18_validation.png", REF_DIR, tmpdir, tol=0.5)

    # Plots the r-z positions of the cell vertices in the layer
    layer.plot_cell_vertices_rz()
    assert save_and_compare("ATLAS_barrel_layer18_cell_vertices_rz.png", REF_DIR, tmpdir, tol=0.5)

    # The thinned down cylinder with infinitesimal dr
    thinned_cyl = layer.get_thinned_cylinder()

    assert pytest.approx(thinned_cyl.rmin) == 2445
    assert pytest.approx(thinned_cyl.rmax) == 2455
    assert pytest.approx(thinned_cyl.zmin) == 3108.202897618112
    assert pytest.approx(thinned_cyl.zmax) == 6221.093028802642


def test_geo_endcap_layer_23(atlas_calo_geo, tmpdir):  # noqa: F811
    layer = GeoLayer(atlas_calo_geo, layer_idx=23)

    assert layer.idx == "23"
    assert layer.coordinate_system == "XYZ"
    assert bool(layer.is_barrel) is False
    assert pytest.approx(layer.extent["rmin"]) == 84.09978870164535
    assert pytest.approx(layer.extent["rmax"]) == 458.8423527799789
    assert pytest.approx(layer.extent["zmin"]) == -6090.100189208984
    assert pytest.approx(layer.extent["zmax"]) == 6090.100189208984

    # Plot layer and envelope in 3D
    layer.plot(thinned=False)
    assert save_and_compare("ATLAS_endcap_layer23_validation.png", REF_DIR, tmpdir, tol=0.5)

    # Plots the r-z positions of the cell vertices in the layer
    layer.plot_cell_vertices_rz()
    assert save_and_compare("ATLAS_endcap_layer23_cell_vertices_rz.png", REF_DIR, tmpdir, tol=0.5)

    # The thinned down cylinder with infinitesimal dz
    thinned_cyl = layer.get_thinned_cylinder()

    assert pytest.approx(thinned_cyl.rmin) == 84.09978870164535
    assert pytest.approx(thinned_cyl.rmax) == 458.8423527799789
    assert pytest.approx(thinned_cyl.zmin) == 5863.9501953125
    assert pytest.approx(thinned_cyl.zmax) == 5873.9501953125
