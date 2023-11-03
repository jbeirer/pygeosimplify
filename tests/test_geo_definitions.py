import numpy as np
import pytest

from pygeosimplify.coordinate.definitions import XYZ, EtaPhiR, EtaPhiZ, RPhiZ
from pygeosimplify.geo.base import Cell, RectangularCell, VertexSet
from pygeosimplify.geo.cells import EtaPhiRCell, EtaPhiZCell, RPhiZCell, XYZCell


def test_vertex_set():
    vertices = np.array([[0, 0], [1, 1], [2, 2]])
    vertex_set = VertexSet(vertices)

    assert np.array_equal(vertex_set.vertices, vertices)


def test_add_vertex_set():
    vertices1 = np.array([[0, 0], [1, 1], [2, 2]])
    vertices2 = np.array([[3, 3], [4, 4], [5, 5]])
    vertex_set1 = VertexSet(vertices1)
    vertex_set2 = VertexSet(vertices2)
    vertex_set3 = vertex_set1 + vertex_set2

    expected_vertices = np.vstack((vertices1, vertices2))
    assert np.array_equal(vertex_set3.vertices, expected_vertices)

    vertex_set4 = vertex_set1 + VertexSet(None)
    assert np.array_equal(vertex_set4.vertices, vertices1)

    vertex_set5 = VertexSet(None) + vertex_set2
    assert np.array_equal(vertex_set5.vertices, vertices2)


def test_cell():
    vertices = np.array([[0, 0, 0], [1, 2, 3], [4, 5, 6], [7, 8, 9]])

    cell = Cell(vertices)
    assert cell.max_extent_in_dim(0) == [0, 7]
    assert cell.max_extent_in_dim(1) == [0, 8]
    assert cell.max_extent_in_dim(2) == [0, 9]

    assert cell.max_extent() == ([0, 7], [0, 8], [0, 9])


def cell():
    # Test that set_vertices sets the vertices correctly
    cell = RectangularCell(2, 3, 4, XYZ(1, 2, 3))
    expected_vertices = np.array(
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
    np.testing.assert_array_equal(cell.vertices, expected_vertices)


def test_XYZ_cell_nominal():
    cell = XYZCell(2, 3, 4, XYZ(1, 2, 3))
    expected_vertices = np.array(
        [
            XYZ(0.0, 0.5, 1.0),
            XYZ(2.0, 0.5, 1.0),
            XYZ(2.0, 3.5, 1.0),
            XYZ(0.0, 3.5, 1.0),
            XYZ(0.0, 0.5, 5.0),
            XYZ(2.0, 0.5, 5.0),
            XYZ(2.0, 3.5, 5.0),
            XYZ(0.0, 3.5, 5.0),
        ]
    )

    np.testing.assert_array_equal(cell.vertices, expected_vertices)
    assert cell.dx == 2
    assert cell.dy == 3
    assert cell.dz == 4
    assert cell.pos == XYZ(1, 2, 3)


def test_XYZ_cell_from_vertices():
    vertices = np.array(
        [
            XYZ(0.0, 0.5, 1.0),
            XYZ(2.0, 0.5, 1.0),
            XYZ(2.0, 3.5, 1.0),
            XYZ(0.0, 3.5, 1.0),
            XYZ(0.0, 0.5, 5.0),
            XYZ(2.0, 0.5, 5.0),
            XYZ(2.0, 3.5, 5.0),
            XYZ(0.0, 3.5, 5.0),
        ]
    )
    cell = XYZCell.create_from_vertices(vertices)
    assert np.all(cell.vertices == vertices)


def test_XYZ_cell_from_vertices_wrong_type():
    with pytest.raises(ValueError):
        vertices = np.array([(1, 2, 3), (4, 5, 6), (7, 8, 9)])
        XYZCell.create_from_vertices(vertices)


def test_RPhiZ_cell_nominal():
    cell = RPhiZCell(2, 3, 4, RPhiZ(1, 2, 3))
    expected_vertices = np.array(
        [
            RPhiZ(0.0, 0.5, 1.0),
            RPhiZ(2.0, 0.5, 1.0),
            RPhiZ(2.0, 3.5, 1.0),
            RPhiZ(0.0, 3.5, 1.0),
            RPhiZ(0.0, 0.5, 5.0),
            RPhiZ(2.0, 0.5, 5.0),
            RPhiZ(2.0, 3.5, 5.0),
            RPhiZ(0.0, 3.5, 5.0),
        ]
    )

    np.testing.assert_array_equal(cell.vertices, expected_vertices)
    assert cell.dr == 2
    assert cell.dphi == 3
    assert cell.dz == 4
    assert cell.pos == RPhiZ(1, 2, 3)


def test_RPhiZ_cell_from_vertices():
    vertices = np.array(
        [
            RPhiZ(0.0, 0.5, 1.0),
            RPhiZ(2.0, 0.5, 1.0),
            RPhiZ(2.0, 3.5, 1.0),
            RPhiZ(0.0, 3.5, 1.0),
            RPhiZ(0.0, 0.5, 5.0),
            RPhiZ(2.0, 0.5, 5.0),
            RPhiZ(2.0, 3.5, 5.0),
            RPhiZ(0.0, 3.5, 5.0),
        ]
    )
    cell = RPhiZCell.create_from_vertices(vertices)
    assert np.all(cell.vertices == vertices)


def test_RPhiZ_cell_from_vertices_wrong_type():
    with pytest.raises(ValueError):
        vertices = np.array([(1, 2, 3), (4, 5, 6), (7, 8, 9)])
        RPhiZCell.create_from_vertices(vertices)


def test_EtaPhiR_cell_nominal():
    cell = EtaPhiRCell(2, 3, 4, EtaPhiR(1, 2, 3))
    expected_vertices = np.array(
        [
            EtaPhiR(0.0, 0.5, 1.0),
            EtaPhiR(2.0, 0.5, 1.0),
            EtaPhiR(2.0, 3.5, 1.0),
            EtaPhiR(0.0, 3.5, 1.0),
            EtaPhiR(0.0, 0.5, 5.0),
            EtaPhiR(2.0, 0.5, 5.0),
            EtaPhiR(2.0, 3.5, 5.0),
            EtaPhiR(0.0, 3.5, 5.0),
        ]
    )

    np.testing.assert_array_equal(cell.vertices, expected_vertices)
    assert cell.deta == 2
    assert cell.dphi == 3
    assert cell.dr == 4
    assert cell.pos == EtaPhiR(1, 2, 3)


def test_EtaPhiR_cell_from_vertices():
    vertices = np.array(
        [
            EtaPhiR(0.0, 0.5, 1.0),
            EtaPhiR(2.0, 0.5, 1.0),
            EtaPhiR(2.0, 3.5, 1.0),
            EtaPhiR(0.0, 3.5, 1.0),
            EtaPhiR(0.0, 0.5, 5.0),
            EtaPhiR(2.0, 0.5, 5.0),
            EtaPhiR(2.0, 3.5, 5.0),
            EtaPhiR(0.0, 3.5, 5.0),
        ]
    )
    cell = EtaPhiRCell.create_from_vertices(vertices)
    assert np.all(cell.vertices == vertices)


def test_EtaPhiR_cell_from_vertices_wrong_type():
    with pytest.raises(ValueError):
        vertices = np.array([(1, 2, 3), (4, 5, 6), (7, 8, 9)])
        EtaPhiRCell.create_from_vertices(vertices)


def test_EtaPhiZ_cell_nominal():
    cell = EtaPhiZCell(2, 3, 4, EtaPhiZ(1, 2, 3))
    expected_vertices = np.array(
        [
            EtaPhiZ(0.0, 0.5, 1.0),
            EtaPhiZ(2.0, 0.5, 1.0),
            EtaPhiZ(2.0, 3.5, 1.0),
            EtaPhiZ(0.0, 3.5, 1.0),
            EtaPhiZ(0.0, 0.5, 5.0),
            EtaPhiZ(2.0, 0.5, 5.0),
            EtaPhiZ(2.0, 3.5, 5.0),
            EtaPhiZ(0.0, 3.5, 5.0),
        ]
    )

    np.testing.assert_array_equal(cell.vertices, expected_vertices)
    assert cell.deta == 2
    assert cell.dphi == 3
    assert cell.dz == 4
    assert cell.pos == EtaPhiZ(1, 2, 3)


def test_EtaPhiZ_cell_from_vertices():
    vertices = np.array(
        [
            EtaPhiZ(0.0, 0.5, 1.0),
            EtaPhiZ(2.0, 0.5, 1.0),
            EtaPhiZ(2.0, 3.5, 1.0),
            EtaPhiZ(0.0, 3.5, 1.0),
            EtaPhiZ(0.0, 0.5, 5.0),
            EtaPhiZ(2.0, 0.5, 5.0),
            EtaPhiZ(2.0, 3.5, 5.0),
            EtaPhiZ(0.0, 3.5, 5.0),
        ]
    )
    cell = EtaPhiZCell.create_from_vertices(vertices)
    assert np.all(cell.vertices == vertices)


def test_EtaPhiZ_cell_from_vertices_wrong_type():
    with pytest.raises(ValueError):
        vertices = np.array([(1, 2, 3), (4, 5, 6), (7, 8, 9)])
        EtaPhiZCell.create_from_vertices(vertices)


def test_XYZ_to_RPhiZ():
    cell = XYZCell(2, 3, 4, XYZ(1, 2, 3))
    expected_vertices = np.array(
        [
            RPhiZ(0.5, 1.57079633, 1.0),
            RPhiZ(2.06155281, 0.24497866, 1.0),
            RPhiZ(4.03112887, 1.05165021, 1.0),
            RPhiZ(3.5, 1.57079633, 1.0),
            RPhiZ(0.5, 1.57079633, 5.0),
            RPhiZ(2.06155281, 0.24497866, 5.0),
            RPhiZ(4.03112887, 1.05165021, 5.0),
            RPhiZ(3.5, 1.57079633, 5.0),
        ]
    )
    np.testing.assert_array_almost_equal(cell.to_RPhiZ().vertices, expected_vertices)


def test_EtaPhiR_to_XYZ():
    cell = EtaPhiRCell(2, 3, 4, EtaPhiR(1, 2, 3))
    expected_vertices = np.array(
        [
            XYZ(0.87758256, 0.47942554, 0.0),
            XYZ(0.87758256, 0.47942554, 3.62686041),
            XYZ(-0.93645669, -0.35078323, 3.62686041),
            XYZ(-0.93645669, -0.35078323, 0.0),
            XYZ(4.38791281, 2.39712769, 0.0),
            XYZ(4.38791281, 2.39712769, 18.13430204),
            XYZ(-4.68228344, -1.75391614, 18.13430204),
            XYZ(-4.68228344, -1.75391614, 0.0),
        ]
    )
    np.testing.assert_array_almost_equal(cell.to_XYZ().vertices, expected_vertices)


def test_EtaPhiR_to_RPhiZ():
    cell = EtaPhiRCell(2, 3, 4, EtaPhiR(1, 2, 3))
    expected_vertices = np.array(
        [
            RPhiZ(1.0, 0.5, 0.0),
            RPhiZ(1.0, 0.5, 3.62686041),
            RPhiZ(1.0, 3.5, 3.62686041),
            RPhiZ(1.0, 3.5, 0.0),
            RPhiZ(5.0, 0.5, 0.0),
            RPhiZ(5.0, 0.5, 18.13430204),
            RPhiZ(5.0, 3.5, 18.13430204),
            RPhiZ(5.0, 3.5, 0.0),
        ]
    )
    np.testing.assert_array_almost_equal(cell.to_RPhiZ().vertices, expected_vertices)


def test_EtaPhiZ_to_XYZ():
    cell = EtaPhiZCell(0.2, 3, 4, EtaPhiZ(0.3, 2, 3.2))
    expected_vertices = np.array(
        [
            XYZ(5.2305552, 2.85746533, 1.2),
            XYZ(2.56382985, 1.40062663, 1.2),
            XYZ(-2.73582876, -1.02480217, 1.2),
            XYZ(-5.58145593, -2.09073324, 1.2),
            XYZ(22.66573918, 12.38234975, 5.2),
            XYZ(11.10992935, 6.06938207, 5.2),
            XYZ(-11.85525795, -4.44080939, 5.2),
            XYZ(-24.18630902, -9.05984405, 5.2),
        ]
    )
    np.testing.assert_array_almost_equal(cell.to_XYZ().vertices, expected_vertices)


def test_EtaPhiZ_to_RPhiZ():
    cell = EtaPhiZCell(0.2, 3, 4, EtaPhiZ(0.3, 2, 3.2))
    expected_vertices = np.array(
        [
            RPhiZ(5.96018588, 0.5, 1.2),
            RPhiZ(2.92146855, 0.5, 1.2),
            RPhiZ(2.92146855, 3.5, 1.2),
            RPhiZ(5.96018588, 3.5, 1.2),
            RPhiZ(25.82747216, 0.5, 5.2),
            RPhiZ(12.65969703, 0.5, 5.2),
            RPhiZ(12.65969703, 3.5, 5.2),
            RPhiZ(25.82747216, 3.5, 5.2),
        ]
    )
    np.testing.assert_array_almost_equal(cell.to_RPhiZ().vertices, expected_vertices)
