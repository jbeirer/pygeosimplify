import numpy as np
from helpers import save_and_compare
from test_load_geo import test_load_geometry as atlas_calo_geo  # noqa: F401

import pygeosimplify as pgs
from pygeosimplify.cfg.test_data import REF_DIR


def test_plot_ATLAS_calo(atlas_calo_geo, tmpdir):  # noqa: F811
    pgs.plot_geometry(
        atlas_calo_geo, phi_range=[0, 0.1], eta_range=[-5, 5], axis_labels=["x [m]", "y [m]", "z [m]"], unit_scale=0.001
    )

    assert save_and_compare("full_ATLAS_calo_phi_0_0.1.png", REF_DIR, tmpdir, tol=0.5)


def test_plot_ATLAS_calo_layer_0(atlas_calo_geo, tmpdir):  # noqa: F811
    pgs.plot_geometry(
        atlas_calo_geo,
        layer_list=[0],
        eta_range=[-5, 5],
        phi_range=[0, np.pi],
        axis_labels=["x [m]", "y [m]", "z [m]"],
        unit_scale=0.001,
    )

    assert save_and_compare("ATLAS_calo_layer_0_phi_0_2pi.png", REF_DIR, tmpdir, tol=0.5)
