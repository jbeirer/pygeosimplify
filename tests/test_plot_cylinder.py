import matplotlib.pyplot as plt
import pytest
from matplotlib.testing.compare import compare_images

from pygeosimplify.cfg.test_data import REF_DIR
from pygeosimplify.simplify.cylinder import Cylinder
from pygeosimplify.vis.cylinder import plot_cylinder


def test_plot_cylinder(tmpdir):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")
    cyl = Cylinder(rmin=0.9, rmax=1, zmin=-1, zmax=1, is_barrel=True)
    plot_cylinder(cyl, color="tab:orange", ax=ax, alpha=0.2)
    plt.savefig(f"{tmpdir}/test.png", dpi=300)
    assert compare_images(f"{REF_DIR}/cylinder.png", f"{tmpdir}/test.png", tol=0.5) is None
    plt.close(fig)


def test_plot_invalid_cylinder():
    # invalid z hierarchy
    with pytest.raises(Exception):
        cyl = Cylinder(rmin=0, rmax=1, zmin=0, zmax=-1, is_barrel=True)
        plot_cylinder(cyl)
    # invalid r hierarchy
    with pytest.raises(Exception):
        cyl = Cylinder(rmin=1, rmax=0, zmin=0, zmax=1, is_barrel=True)
        plot_cylinder(cyl)
