<img src=https://github.com/jbeirer/pygeosimplify/raw/main/docs/logo.svg alt="Logo" width="250">


[![Release](https://img.shields.io/github/v/release/jbeirer/pygeosimplify)](https://img.shields.io/github/v/release/jbeirer/pygeosimplify)
[![Build status](https://img.shields.io/github/actions/workflow/status/jbeirer/pygeosimplify/main.yml?branch=main)](https://github.com/jbeirer/pygeosimplify/actions/workflows/main.yml?query=branch%3Amain)
[![codecov](https://codecov.io/gh/jbeirer/pygeosimplify/graph/badge.svg?token=ZCJV384TXF)](https://codecov.io/gh/jbeirer/pygeosimplify)
[![Commit activity](https://img.shields.io/github/commit-activity/m/jbeirer/pygeosimplify)](https://img.shields.io/github/commit-activity/m/jbeirer/pygeosimplify)
[![License](https://img.shields.io/github/license/jbeirer/pygeosimplify)](https://img.shields.io/github/license/jbeirer/pygeosimplify)
[![DOI](https://zenodo.org/badge/707731497.svg)](https://doi.org/10.5281/zenodo.14308339)


Welcome to pyGeoSimplify!

## Download pyGeoSimplify
```python
pip install pygeosimplify
```

## Quick Start

```python
import pygeosimplify as pgs
from pygeosimplify.simplify.layer import GeoLayer
from pygeosimplify.simplify.detector import SimplifiedDetector

# Set names of branches that specify coordinate system of cells
pgs.set_coordinate_branch("XYZ", "isCartesian")

# Load geometry
geo = pgs.load_geometry("DetectorCells.root", tree_name='treeName')

# Create simplified detector
detector = SimplifiedDetector()

# Add dector layers to detector
layer = GeoLayer(geo, layer_idx)
detector.add_layer(layer)

# Process detector
detector.process()

# Save simplified detector to gdml file
detector.save_to_gdml(cyl_type='processed', output_path='processed.gdml')
```

## LICENSE

pyGeoSimplify is free of use and open-source. All versions are
published under the [MIT License](https://github.com/jbeirer/pygeosimplify/blob/main/LICENSE).
