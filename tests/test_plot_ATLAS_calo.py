import matplotlib.pyplot as plt
import numpy as np
from matplotlib.testing.compare import compare_images

import pygeosimplify as pgs
from pygeosimplify.cfg.test_data import REF_DIR


def test_plot_ATLAS_calo(atlas_calo_geo, tmpdir):
    pgs.plot_geometry(
        atlas_calo_geo, phi_range=[0, 0.1], eta_range=[-5, 5], axis_labels=["x [m]", "y [m]", "z [m]"], unit_scale=0.001
    )

    plt.savefig(f"{tmpdir}/test.png", dpi=300)
    assert compare_images(f"{REF_DIR}/full_ATLAS_calo_phi_0_0.1.png", f"{tmpdir}/test.png", tol=0) is None


def test_plot_ATLAS_calo_layer_0(atlas_calo_geo, tmpdir):
    pgs.plot_geometry(
        atlas_calo_geo,
        layer_list=[0],
        eta_range=[-5, 5],
        phi_range=[0, np.pi],
        axis_labels=["x [m]", "y [m]", "z [m]"],
        unit_scale=0.001,
    )

    plt.savefig(f"{tmpdir}/test.png", dpi=300)
    assert compare_images(f"{REF_DIR}/ATLAS_calo_layer_0_phi_0_2pi.png", f"{tmpdir}/test.png", tol=0) is None
