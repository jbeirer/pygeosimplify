import os

import pytest
from test_load_geo import test_load_geometry as atlas_calo_geo  # noqa: F401

from pygeosimplify.simplify.detector import SimplifiedDetector
from pygeosimplify.simplify.layer import GeoLayer


def test_add_layer(atlas_calo_geo):  # noqa: F811
    detector = SimplifiedDetector(min_layer_dist=1, envelope_width=100)
    layer = GeoLayer(atlas_calo_geo, layer_idx=9)
    detector.add_layer(layer)

    assert layer.idx in detector.layers
    assert layer.idx in detector.cylinders.envelope
    assert layer.idx in detector.cylinders.thinned
    assert detector.processed == False
    assert detector.min_dist == 1
    assert detector.envelope_width == 100

    envelope = detector.cylinders.envelope[layer.idx]
    assert pytest.approx(envelope.rmin, abs=1e-3) == 425.2125616816107
    assert pytest.approx(envelope.rmax, abs=1e-3) == 2329.110247656521
    assert pytest.approx(envelope.zmin, abs=1e-3) == 4735.5
    assert pytest.approx(envelope.zmax, abs=1e-3) == 5003.5
    assert envelope.is_barrel == False

    thinned = detector.cylinders.thinned[layer.idx]
    assert pytest.approx(thinned.rmin, abs=1e-3) == 425.2125616816107
    assert pytest.approx(thinned.rmax, abs=1e-3) == 2329.110247656521
    assert pytest.approx(thinned.zmin, abs=1e-3) == 4864.5
    assert pytest.approx(thinned.zmax, abs=1e-3) == 4874.5


def test_add_layer_duplicate(atlas_calo_geo):  # noqa: F811
    detector = SimplifiedDetector()
    layer = GeoLayer(atlas_calo_geo, layer_idx=10)
    detector.add_layer(layer)

    with pytest.raises(Exception):
        detector.add_layer(layer)


def test_process(atlas_calo_geo):  # noqa: F811
    detector = SimplifiedDetector()
    layer_list = [0, 4, 21]
    for layer_idx in layer_list:
        layer = GeoLayer(atlas_calo_geo, layer_idx)
        detector.add_layer(layer)
    detector.process()

    assert detector.processed == True
    assert pytest.approx(detector.cylinders.processed["0_POS"].rmin, abs=1e-3) == 1451.6619
    assert pytest.approx(detector.cylinders.processed["0_POS"].rmax, abs=1e-3) == 1461.6619
    assert pytest.approx(detector.cylinders.processed["0_POS"].zmin, abs=1e-3) == 0.0
    assert pytest.approx(detector.cylinders.processed["0_POS"].zmax, abs=1e-3) == 3663.0
    assert detector.cylinders.processed["0_POS"].is_barrel == True

    assert pytest.approx(detector.cylinders.processed["21_POS"].rmin, abs=1e-3) == 69.9850
    assert pytest.approx(detector.cylinders.processed["21_POS"].rmax, abs=1e-3) == 1702.5874
    assert pytest.approx(detector.cylinders.processed["21_POS"].zmin, abs=1e-3) == 4824.5500
    assert pytest.approx(detector.cylinders.processed["21_POS"].zmax, abs=1e-3) == 4940.600
    assert detector.cylinders.processed["21_POS"].is_barrel == False

    assert pytest.approx(detector.cylinders.processed["4_POS"].rmin, abs=1e-3) == 69.9850
    assert pytest.approx(detector.cylinders.processed["4_POS"].rmax, abs=1e-3) == 1702.5874
    assert pytest.approx(detector.cylinders.processed["4_POS"].zmin, abs=1e-3) == 3668.0
    assert pytest.approx(detector.cylinders.processed["4_POS"].zmax, abs=1e-3) == 3670.0
    assert detector.cylinders.processed["4_POS"].is_barrel == False

    assert pytest.approx(detector.cylinders.processed["0_NEG"].rmin, abs=1e-3) == 1451.6619
    assert pytest.approx(detector.cylinders.processed["0_NEG"].rmax, abs=1e-3) == 1461.6619
    assert pytest.approx(detector.cylinders.processed["0_NEG"].zmin, abs=1e-3) == -3663.0
    assert pytest.approx(detector.cylinders.processed["0_NEG"].zmax, abs=1e-3) == 0.0
    assert detector.cylinders.processed["0_NEG"].is_barrel == True

    assert pytest.approx(detector.cylinders.processed["21_NEG"].rmin, abs=1e-3) == 69.9850194
    assert pytest.approx(detector.cylinders.processed["21_NEG"].rmax, abs=1e-3) == 1702.58747
    assert pytest.approx(detector.cylinders.processed["21_NEG"].zmin, abs=1e-3) == -4940.6000
    assert pytest.approx(detector.cylinders.processed["21_NEG"].zmax, abs=1e-3) == -4824.5500
    assert detector.cylinders.processed["21_NEG"].is_barrel == False

    assert pytest.approx(detector.cylinders.processed["4_NEG"].rmin, abs=1e-3) == 69.9850
    assert pytest.approx(detector.cylinders.processed["4_NEG"].rmax, abs=1e-3) == 1702.587
    assert pytest.approx(detector.cylinders.processed["4_NEG"].zmin, abs=1e-3) == -3670.0
    assert pytest.approx(detector.cylinders.processed["4_NEG"].zmax, abs=1e-3) == -3668.0
    assert detector.cylinders.processed["4_NEG"].is_barrel == False


def test_process_already_processed(atlas_calo_geo):  # noqa: F811
    detector = SimplifiedDetector()
    layer = GeoLayer(atlas_calo_geo, layer_idx=9)
    detector.add_layer(layer)
    detector.process()

    with pytest.raises(Exception):
        detector.process()


def test_check_overlaps(atlas_calo_geo):  # noqa: F811
    detector = SimplifiedDetector()
    layer2 = GeoLayer(atlas_calo_geo, layer_idx=2)
    layer3 = GeoLayer(atlas_calo_geo, layer_idx=3)
    detector.add_layer(layer2)
    detector.add_layer(layer3)
    detector.process()

    # Envelopes should overlap
    n_overlaps, overlapping_layers = detector.check_overlaps(cyl_type="envelope")
    assert n_overlaps == 2
    assert overlapping_layers == [["2_POS", "3_POS"], ["2_NEG", "3_NEG"]]
    # # Thinned cylinders should not overlap
    n_overlaps, overlapping_layers = detector.check_overlaps(cyl_type="thinned")
    assert n_overlaps == 0
    assert overlapping_layers == []


def test_save_to_gdml(atlas_calo_geo, tmpdir):  # noqa: F811
    detector = SimplifiedDetector()
    layer = GeoLayer(atlas_calo_geo, layer_idx=9)
    detector.add_layer(layer)

    # Save to gdml before processing
    with pytest.raises(Exception):
        detector.save_to_gdml(output_path=f"{tmpdir}/simplified_detector.gdml")

    detector.process()

    output_path = f"{tmpdir}/simplified_detector.gdml"
    detector.save_to_gdml(output_path=output_path)

    assert os.path.exists(output_path)
