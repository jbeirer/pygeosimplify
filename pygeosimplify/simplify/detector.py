from typing import Tuple

from pyg4ometry.gdml import Writer
from pyg4ometry.geant4 import MaterialPredefined

from pygeosimplify.simplify.cylinder import Cylinder, CylinderGroup
from pygeosimplify.simplify.helpers import add_cylinder_dict_to_reg, check_pairwise_overlaps, init_world
from pygeosimplify.simplify.layer import GeoLayer
from pygeosimplify.simplify.post_process import post_process_cylinders


class SimplifiedDetector:
    def __init__(self) -> None:
        self.layers = {}  # type: dict[str, GeoLayer]
        self.cylinders = CylinderGroup()
        self.processed = False
        self.envelope = {}  # type: dict[str, Cylinder]

    def _get_cylinder_dict(self, cyl_type: str) -> dict[str, Cylinder]:
        if cyl_type not in ["thinned", "envelope", "processed"]:
            raise Exception(f"Invalid cylinder type {cyl_type}. Must be one of: thinned, cell_envelope, post_processed")

        cyl_dict = getattr(self.cylinders, cyl_type)  # type: dict[str, Cylinder]

        return cyl_dict

    def _resolve_thinned_overlaps(self) -> None:
        # Note: needs to be expanded to address potential overlaps of thinned layers
        # Currently a dirty fix to address overlap of layer 2,5 in thinned ATLAS layers

        n_overlaps, overlapping_layers = self.check_overlaps(cyl_type="thinned", print_output=False)

        if n_overlaps > 0:
            for overlap_pair in overlapping_layers:
                if overlap_pair == ["Layer_2", "Layer_5"]:
                    self.cylinders.thinned["2"].zmax = (
                        self.cylinders.thinned["2"].zmax - 0.01 * self.cylinders.thinned["2"].zmax
                    )

    def _symmetrize_cylinders(self, cyl_type: str = "thinned") -> dict[str, Cylinder]:
        # Get the dimensions for the requested cylinder type
        cyl_dict_pos_z = self._get_cylinder_dict(cyl_type)
        cyl_dict_neg_z = {}

        # Create the negative z cylinders from the positive halfspace
        for idx, cyl in cyl_dict_pos_z.items():
            if self.layers[idx].is_continuous_in_z():
                cyl.zmin = 0

            neg_z_cyl = Cylinder(cyl.rmin, cyl.rmax, -cyl.zmax, -cyl.zmin, cyl.is_barrel)
            cyl_dict_neg_z[idx] = neg_z_cyl

        cyl_dict_pos_z = {str(idx) + "_POS": cyl for idx, cyl in sorted(cyl_dict_pos_z.items())}
        cyl_dict_neg_z = {str(idx) + "_NEG": cyl for idx, cyl in sorted(cyl_dict_neg_z.items())}

        return {**cyl_dict_pos_z, **cyl_dict_neg_z}

    def add_layer(self, layer: GeoLayer) -> None:
        # Ensure that the layer does not already exist in the simplified detector
        if layer.idx in self.cylinders.thinned:
            raise Exception(f"Layer {layer.idx} already exists in the simplified detector")

        # Add layer to the layer dictionary
        self.layers[layer.idx] = layer
        # Set layer envelope
        self.cylinders.envelope[layer.idx] = layer.get_cell_envelope()
        # Get overlap-resolved thinned cylinders
        self.cylinders.thinned[layer.idx] = layer.get_thinned_cylinder()

    def process(self) -> None:
        # Resolve thinned cylinder overlaps
        self._resolve_thinned_overlaps()
        # Symmetrize thinned cylinders
        self.cylinders.thinned = self._symmetrize_cylinders(cyl_type="thinned")
        self.cylinders.envelope = self._symmetrize_cylinders(cyl_type="envelope")
        # Grow cylinders
        self.cylinders.processed, self.envelope = post_process_cylinders(
            cyl_dict=self.cylinders.thinned, cell_envelope=self.cylinders.envelope, min_dist=1
        )
        self.processed = True

    def check_overlaps(
        self,
        cyl_type: str = "thinned",
        print_output: bool = True,
        recursive: bool = False,
        coplanar: bool = False,
        debugIO: bool = False,
    ) -> Tuple[int, list[list[str]]]:
        cyl_dict = self._get_cylinder_dict(cyl_type)

        return check_pairwise_overlaps(cyl_dict, print_output, recursive, coplanar, debugIO)

    def save_to_gdml(self, cyl_type: str = "processed", output_path: str = "simplified_detector.gmdl") -> None:
        if not self.processed:
            raise Exception("Detector has not been processed yet. Process first with detector.process()")

        # Get the dimensions for the requested cylinder type
        cyl_dict = self._get_cylinder_dict(cyl_type)
        # Initialize the world and registry
        world, registry = init_world(MaterialPredefined("G4_Galactic"))
        # Add the cylinder to the registry
        add_cylinder_dict_to_reg(registry, world, cyl_dict, MaterialPredefined("G4_Galactic"))
        # Add envelope of detector
        add_cylinder_dict_to_reg(registry, world, self.envelope, MaterialPredefined("G4_Galactic"))
        # Write the gdml file
        gdml_writer = Writer()
        gdml_writer.addDetector(registry)
        gdml_writer.write(output_path)
