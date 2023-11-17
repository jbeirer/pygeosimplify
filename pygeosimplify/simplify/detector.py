from typing import Tuple

from pyg4ometry.gdml import Writer
from pyg4ometry.geant4 import MaterialPredefined

from pygeosimplify.simplify.cylinder import Cylinder, CylinderGroup
from pygeosimplify.simplify.helpers import add_cylinder_dict_to_reg, check_pairwise_overlaps, init_world
from pygeosimplify.simplify.layer import GeoLayer
from pygeosimplify.simplify.post_process import post_process_cylinders
from pygeosimplify.utils.message_type import MessageType as mt


class SimplifiedDetector:
    def __init__(self) -> None:
        self.layers = {}  # type: dict[str, GeoLayer]
        self.cylinders = CylinderGroup()
        self.processed = False
        self.envelope = {}  # type: dict[str, Cylinder]
        self.min_dist = 1  # mm
        self.envelope_width = 100  # 10 cm

    def _get_cylinder_dict(self, cyl_type: str) -> dict[str, Cylinder]:
        if cyl_type not in ["thinned", "envelope", "processed"]:
            raise Exception(f"Invalid cylinder type {cyl_type}. Must be one of: thinned, cell_envelope, post_processed")

        cyl_dict = getattr(self.cylinders, cyl_type)  # type: dict[str, Cylinder]

        return cyl_dict

    def _resolve_thinned_overlaps(self) -> None:
        n_overlaps, overlapping_layers = self.check_overlaps(cyl_type="thinned", print_output=False)

        if n_overlaps == 0:
            return

        for overlap_pair in overlapping_layers:
            cyl_a_name = overlap_pair[0]
            cyl_b_name = overlap_pair[1]

            cyl_a = self.cylinders.thinned[cyl_a_name]
            cyl_b = self.cylinders.thinned[cyl_b_name]

            if cyl_a.is_barrel and not cyl_b.is_barrel:
                barrel = cyl_a
                endcap = cyl_b
            elif cyl_b.is_barrel and not cyl_a.is_barrel:
                barrel = cyl_b
                endcap = cyl_a
            else:
                raise Exception(
                    f"{mt.FAIL} Overlap between two barrel or two endcap layers detected: {cyl_a_name}, {cyl_b_name}."
                    " This is not supposed to happen."
                )

            print(
                f"{mt.WARNING} Overlap between thinned layer {cyl_a_name} and layer {cyl_b_name}. Attempting to"
                " resolve..."
            )

            # Option A: Shorten the zmax of the barrel layer to the zmin of the endcap layer
            new_barrel_zmax = endcap.zmin - self.min_dist
            opt_A_diff = abs(new_barrel_zmax - barrel.zmax)
            # Option B: Decrease rmax of endcap layer to rmin of barrel layer
            new_endcap_rmax = barrel.rmin - self.min_dist
            opt_B_diff = abs(new_endcap_rmax - endcap.rmax)
            # Option C: Increase rmin of endcap to rmax of barrel layer
            new_encap_rmin = barrel.rmax + self.min_dist
            opt_C_diff = abs(endcap.rmin - new_encap_rmin)

            # Use option with minimal change
            if opt_A_diff < opt_B_diff and opt_A_diff < opt_C_diff:
                print(f"{mt.BOLD} Setting barrel zmax from {barrel.zmax} to {new_barrel_zmax}")
                barrel.zmax = new_barrel_zmax
            elif opt_B_diff < opt_A_diff and opt_B_diff < opt_C_diff:
                print(f"{mt.BOLD} Setting endcap rmax from {endcap.rmax} to {new_endcap_rmax}")
                endcap.rmax = new_endcap_rmax
            else:
                print(f"{mt.BOLD} Setting endcap rmin from {endcap.rmin} to {new_encap_rmin}")
                endcap.rmin = new_encap_rmin

            # Update the thinned cylinder dictionary
            self.cylinders.thinned[cyl_a_name] = barrel if cyl_a.is_barrel else endcap
            self.cylinders.thinned[cyl_b_name] = barrel if cyl_b.is_barrel else endcap

        # Check if overlaps have been resolved
        n_overlaps, _ = self.check_overlaps(cyl_type="thinned", print_output=False)

        if n_overlaps > 0:
            raise Exception(
                f"{mt.FAIL} Overlap resolution of thinned cylinders failed. {n_overlaps} overlaps remain. This is not"
                " supposed to happen."
            )
        else:
            print(f"{mt.SUCCESS} Thinned cylinder overlaps resolved.")

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
        if self.processed:
            raise Exception("Detector has already been processed. Cowardly refusing to re-process...")

        self.processed = True
        # Resolve thinned cylinder overlaps
        self._resolve_thinned_overlaps()
        # Symmetrize thinned cylinders
        self.cylinders.thinned = self._symmetrize_cylinders(cyl_type="thinned")
        self.cylinders.envelope = self._symmetrize_cylinders(cyl_type="envelope")
        # Grow cylinders
        self.cylinders.processed, self.envelope = post_process_cylinders(
            cyl_dict=self.cylinders.thinned,
            cell_envelope=self.cylinders.envelope,
            min_dist=self.min_dist,
            envelope_width=self.envelope_width,
        )

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
