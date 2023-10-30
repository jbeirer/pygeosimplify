import unittest

from pygeosimplify.coordinate.definitions import XYZ, EtaPhiR, EtaPhiZ


class TestCoordinateTransform(unittest.TestCase):
    def test_XYZ_to_RPhiZ(self):
        xyz = XYZ(1, 2, 3)
        rphiz = xyz.to_RPhiZ()

        self.assertAlmostEqual(rphiz.r, 2.23606798)
        self.assertAlmostEqual(rphiz.phi, 1.10714872)
        self.assertAlmostEqual(rphiz.z, 3)

    def test_EtaPhiR_to_RPhiZ(self):
        etaphir = EtaPhiR(1, 2, 3)
        rphiz = etaphir.to_RPhiZ()

        self.assertAlmostEqual(rphiz.r, 3)
        self.assertAlmostEqual(rphiz.phi, 2)
        self.assertAlmostEqual(rphiz.z, 3.52560358)

    def test_EtaPhiR_to_XYZ(self):
        etaphir = EtaPhiR(1, 2, 3)
        xyz = etaphir.to_XYZ()

        self.assertAlmostEqual(xyz.x, -1.24844051)
        self.assertAlmostEqual(xyz.y, 2.72789228)
        self.assertAlmostEqual(xyz.z, 3.52560358)

    def test_EtaPhiZ_to_XYZ(self):
        etaphiz = EtaPhiZ(1, 2, 3)
        xyz = etaphiz.to_XYZ()

        self.assertAlmostEqual(xyz.x, -1.06232066)
        self.assertAlmostEqual(xyz.y, 2.32121299)
        self.assertAlmostEqual(xyz.z, 3)

    def test_EtaPhiZ_to_RPhiZ(self):
        etaphiz = EtaPhiZ(1, 2, 3)
        rphiz = etaphiz.to_RPhiZ()

        self.assertAlmostEqual(rphiz.r, 2.55275438)
        self.assertAlmostEqual(rphiz.phi, 2)
        self.assertAlmostEqual(rphiz.z, 3)
