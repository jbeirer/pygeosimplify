import matplotlib.pyplot as plt
import numpy as np
import pytest
from matplotlib.testing.compare import compare_images
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from mpl_toolkits.mplot3d.axes3d import Axes3D
from scipy.spatial._qhull import QhullError

from pygeosimplify.cfg.test_data import REF_DIR
from pygeosimplify.coordinate.definitions import XYZ
from pygeosimplify.geo.base import Cell
from pygeosimplify.geo.cells import XYZCell
from pygeosimplify.vis.scene import CellScene


def test_add_cell():
    cell_scene = CellScene()
    cell = XYZCell(2, 3, 4, XYZ(1, 2, 3))
    cell_scene.add_cell(cell)
    assert cell_scene.n_cells() == 1


def test_clear_cell_list():
    cell_scene = CellScene()
    cell = XYZCell(2, 3, 4, XYZ(1, 2, 3))
    cell_scene.add_cell(cell)
    cell_scene.clear_cell_list()
    assert cell_scene.n_cells() == 0


def test_min_max_cell_list_extent():
    cell_scene = CellScene()
    cell1 = XYZCell(-1, 3, 0, XYZ(1, -2, 3))
    cell2 = XYZCell(2, 3, 4, XYZ(4, 2, 6))
    cell_scene.add_cell(cell1)
    cell_scene.add_cell(cell2)
    assert cell_scene.min_max_cell_list_extent(0) == (0.5, 5)
    assert cell_scene.min_max_cell_list_extent(1) == (-3.5, 3.5)
    assert cell_scene.min_max_cell_list_extent(2) == (3.0, 8.0)


def test_plot_empty_scene():
    cell_scene = CellScene()
    with pytest.raises(RuntimeWarning):
        ax = cell_scene.plot()
        assert isinstance(ax, Axes3D)
        assert ax.get_xlim() == (0, 1)
        assert ax.get_ylim() == (0, 1)
        assert ax.get_zlim() == (0, 1)
        assert len(ax.collections) == 0


def test_plot_invalid_raw_cell():
    cell_scene = CellScene()
    vertices = np.array([[-1, 0, 2]])
    raw_cell = Cell(vertices)
    cell_scene.add_cell(raw_cell)
    axis_limits = [(0, 1), (0, 1), (0, 1)]
    with pytest.raises(QhullError):
        cell_scene.plot(axis_limits=axis_limits)


def test_plot_raw_cell():
    cell_scene = CellScene()
    vertices = np.array(
        [
            [0.0, 0.5, 1.0],
            [2.0, 0.5, 1.0],
            [2.0, 3.5, 1.0],
            [0.0, 3.5, 1.0],
            [0.0, 0.5, 5.0],
            [2.0, 0.5, 5.0],
            [2.0, 3.5, 5.0],
            [0.0, 3.5, 5.0],
        ]
    )
    raw_cell = Cell(vertices)
    cell_scene.add_cell(raw_cell)
    ax = cell_scene.plot(axis_labels=["x", "y", "z"])
    assert isinstance(ax, Axes3D)
    assert ax.get_xlim() == (0, 2)
    assert ax.get_ylim() == (0.5, 3.5)
    assert ax.get_zlim() == (1, 5)
    assert len(ax.collections) == 1
    assert isinstance(ax.collections[0], Poly3DCollection)


def test_plot_single_XYZ_cell(tmpdir):
    cell_scene = CellScene()
    cell = XYZCell(2, 3, 4, XYZ(1, 2, 3))
    cell_scene.add_cell(cell)
    ax = cell_scene.plot(axis_labels=["x", "y", "z"])
    assert isinstance(ax, Axes3D)
    assert ax.get_xlim() == (0, 2)
    assert ax.get_ylim() == (0.5, 3.5)
    assert ax.get_zlim() == (1, 5)
    assert len(ax.collections) == 1
    assert isinstance(ax.collections[0], Poly3DCollection)

    plt.savefig(f"{tmpdir}/test.png", dpi=300, bbox_inches="tight")
    assert compare_images(f"{REF_DIR}/single_XYZ_cell.png", f"{tmpdir}/test.png", tol=0) is None


def test_plot_single_XYZ_cell_with_user_axis():
    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")
    cell_scene = CellScene()
    cell = XYZCell(2, 3, 4, XYZ(1, 2, 3))
    cell_scene.add_cell(cell)
    expected_axis = cell_scene.plot()
    user_axis = cell_scene.plot(ax=ax)

    assert expected_axis.get_xlim() == user_axis.get_xlim()
    assert expected_axis.get_ylim() == user_axis.get_ylim()
    assert expected_axis.get_zlim() == user_axis.get_zlim()
    assert len(expected_axis.collections) == len(user_axis.collections)


def test_plot_multi_XYZ_cells(tmpdir):
    cell_scene = CellScene()
    cell1 = XYZCell(2, 3, 4, XYZ(1, 2, 3))
    cell2 = XYZCell(2, 3, 4, XYZ(4, 5, 6))
    cell_scene.add_cell(cell1)
    cell_scene.add_cell(cell2)
    ax = cell_scene.plot(axis_labels=["x", "y", "z"])
    assert isinstance(ax, Axes3D)
    assert ax.get_xlim() == (0, 5)
    assert ax.get_ylim() == (0.5, 6.5)
    assert ax.get_zlim() == (1, 8)
    assert len(ax.collections) == 2
    assert isinstance(ax.collections[0], Poly3DCollection)
    assert isinstance(ax.collections[1], Poly3DCollection)

    plt.savefig(f"{tmpdir}/test.png", dpi=300, bbox_inches="tight")
    assert compare_images(f"{REF_DIR}/multi_XYZ_cell.png", f"{tmpdir}/test.png", tol=0) is None
