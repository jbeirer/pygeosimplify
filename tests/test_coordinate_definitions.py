import pytest

from pygeosimplify.coordinate.definitions import XYZ, EtaPhiR, EtaPhiZ, RPhiZ


def test_rphiz_getitem():
    rphiz = RPhiZ(1.0, 2.0, 3.0)
    assert rphiz[0] == 1.0
    assert rphiz[1] == 2.0
    assert rphiz[2] == 3.0


def test_rphiz_add():
    rphiz1 = RPhiZ(1.0, 2.0, 3.0)
    rphiz2 = RPhiZ(4.0, 5.0, 6.0)
    rphiz3 = rphiz1 + rphiz2
    assert rphiz3.r == 5.0
    assert rphiz3.phi == 7.0
    assert rphiz3.z == 9.0


def test_rphiz_add_invalid_operand():
    rphiz = RPhiZ(1.0, 2.0, 3.0)
    with pytest.raises(TypeError):
        rphiz + 1


def test_rphiz_sub():
    rphiz1 = RPhiZ(1.0, 2.0, 3.0)
    rphiz2 = RPhiZ(4.0, 5.0, 6.0)
    rphiz3 = rphiz2 - rphiz1
    assert rphiz3.r == 3.0
    assert rphiz3.phi == 3.0
    assert rphiz3.z == 3.0


def test_rphiz_sub_invalid_operand():
    rphiz = RPhiZ(1.0, 2.0, 3.0)
    with pytest.raises(TypeError):
        rphiz - 1


def test_rphiz_abs():
    rphiz = RPhiZ(1.0, 2.0, 3.0)
    assert pytest.approx(abs(rphiz), abs=1e-7) == 3.7416573867739413


def test_XYZ_getitem():
    xyz = XYZ(1.0, 2.0, 3.0)
    assert xyz[0] == 1.0
    assert xyz[1] == 2.0
    assert xyz[2] == 3.0


def test_XYZ_add():
    xyz1 = XYZ(1.0, 2.0, 3.0)
    xyz2 = XYZ(4.0, 5.0, 6.0)
    xyz3 = xyz1 + xyz2
    assert xyz3.x == 5.0
    assert xyz3.y == 7.0
    assert xyz3.z == 9.0


def test_XYZ_add_invalid_operand():
    xyz = XYZ(1.0, 2.0, 3.0)
    with pytest.raises(TypeError):
        xyz + 1


def test_XYZ_sub():
    xyz1 = XYZ(1.0, 2.0, 3.0)
    xyz2 = XYZ(4.0, 5.0, 6.0)
    xyz3 = xyz2 - xyz1
    assert xyz3.x == 3.0
    assert xyz3.y == 3.0
    assert xyz3.z == 3.0


def test_XYZ_sub_invalid_operand():
    xyz = XYZ(1.0, 2.0, 3.0)
    with pytest.raises(TypeError):
        xyz - 1


def test_XYZ_abs():
    xyz = XYZ(1.0, 2.0, 3.0)
    assert pytest.approx(abs(xyz), abs=1e-7) == 3.7416573867739413


def test_etaphir_getitem():
    etaphir = EtaPhiR(1.0, 2.0, 3.0)
    assert etaphir[0] == 1.0
    assert etaphir[1] == 2.0
    assert etaphir[2] == 3.0


def test_etaphir_add():
    etaphir1 = EtaPhiR(1.0, 2.0, 3.0)
    etaphir2 = EtaPhiR(4.0, 5.0, 6.0)
    etaphir3 = etaphir1 + etaphir2
    assert etaphir3.eta == 5.0
    assert etaphir3.phi == 7.0
    assert etaphir3.r == 9.0


def test_etaphir_add_invalid_operand():
    etaphir = EtaPhiR(1.0, 2.0, 3.0)
    with pytest.raises(TypeError):
        etaphir + 1


def test_etaphir_sub():
    etaphir1 = EtaPhiR(1.0, 2.0, 3.0)
    etaphir2 = EtaPhiR(4.0, 5.0, 6.0)
    etaphir3 = etaphir2 - etaphir1
    assert etaphir3.eta == 3.0
    assert etaphir3.phi == 3.0
    assert etaphir3.r == 3.0


def test_etaphir_sub_invalid_operand():
    etaphir = EtaPhiR(1.0, 2.0, 3.0)
    with pytest.raises(TypeError):
        etaphir - 1


def test_etaphir_abs():
    etaphir = EtaPhiR(1.0, 2.0, 3.0)
    assert pytest.approx(abs(etaphir), abs=1e-7) == 3.7416573867739413


def test_etaphiz_getitem():
    etaphiz = EtaPhiZ(1.0, 2.0, 3.0)
    assert etaphiz[0] == 1.0
    assert etaphiz[1] == 2.0
    assert etaphiz[2] == 3.0


def test_etaphiz_add():
    etaphiz1 = EtaPhiZ(1.0, 2.0, 3.0)
    etaphiz2 = EtaPhiZ(4.0, 5.0, 6.0)
    etaphiz3 = etaphiz1 + etaphiz2
    assert etaphiz3.eta == 5.0
    assert etaphiz3.phi == 7.0
    assert etaphiz3.z == 9.0


def test_etaphiz_add_invalid_operand():
    etaphiz = EtaPhiZ(1.0, 2.0, 3.0)
    with pytest.raises(TypeError):
        etaphiz + 1


def test_etaphiz_sub():
    etaphiz1 = EtaPhiZ(1.0, 2.0, 3.0)
    etaphiz2 = EtaPhiZ(4.0, 5.0, 6.0)
    etaphiz3 = etaphiz2 - etaphiz1
    assert etaphiz3.eta == 3.0
    assert etaphiz3.phi == 3.0
    assert etaphiz3.z == 3.0


def test_etaphiz_sub_invalid_operand():
    etaphiz = EtaPhiZ(1.0, 2.0, 3.0)
    with pytest.raises(TypeError):
        etaphiz - 1


def test_etaphiz_abs():
    etaphiz = EtaPhiZ(1.0, 2.0, 3.0)
    assert pytest.approx(abs(etaphiz), abs=1e-7) == 3.7416573867739413
