from pyg4ometry.gdml import Writer
from pyg4ometry.geant4 import MaterialPredefined

from pygeosimplify.simplify.cylinder import Cylinder, CylinderGroup
from pygeosimplify.simplify.helpers import add_cylinder_dict_to_reg, check_pairwise_overlaps, init_world
from pygeosimplify.simplify.layer import GeoLayer
from pygeosimplify.simplify.post_process import post_process_cylinders
from pygeosimplify.utils.message_type import MessageType as mt


class SimplifiedDetector:
    def __init__(self, min_layer_dist: float = 1, envelope_width: float = 100) -> None:
        self.is_layer_continuous_in_z = {}  # type: dict[str, bool]
        self.cylinders = CylinderGroup()
        self.processed = False
        self.envelope = {}  # type: dict[str, Cylinder]
        self.min_dist = min_layer_dist
        self.envelope_width = envelope_width

    def _get_cylinder_dict(self, cyl_type: str) -> dict[str, Cylinder]:
        if cyl_type not in ["thinned", "envelope", "processed"]:
            raise Exception(f"Invalid cylinder type {cyl_type}. Must be one of: thinned, cell_envelope, post_processed")

        cyl_dict = getattr(self.cylinders, cyl_type)  # type: dict[str, Cylinder]

        return cyl_dict

    def _resolve_thinned_overlaps(self) -> None:
        n_overlaps, overlapping_layers = self.check_overlaps(cyl_type="thinned", print_output=False)

        if n_overlaps == 0:
            return

        while n_overlaps > 0:
            # Take the first overlapping pair
            overlap_pair = overlapping_layers[0]
            # Take the cylinders from the overlapping pair
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

            # Calculate new values and their differences
            options = [
                {
                    "name": (
                        f"Option A: Shorten the zmax of the barrel layer ({barrel.zmax}) to the zmin of the endcap"
                        f" layer ({endcap.zmin - self.min_dist})"
                    ),
                    "diff": abs((endcap.zmin - self.min_dist) - barrel.zmax),
                    "locked": barrel.is_locked("zmax"),
                    "action": lambda barrel=barrel, endcap=endcap: (
                        setattr(barrel, "zmax", endcap.zmin - self.min_dist),  # type: ignore[func-returns-value]
                        barrel.lock("zmax"),
                    ),
                },
                {
                    "name": (
                        f"Option B: Decrease rmax of endcap layer ({endcap.rmax}) to rmin of barrel layer"
                        f" ({barrel.rmin - self.min_dist})"
                    ),
                    "diff": abs((barrel.rmin - self.min_dist) - endcap.rmax),
                    "locked": endcap.is_locked("rmax"),
                    "action": lambda barrel=barrel, endcap=endcap: (
                        setattr(endcap, "rmax", barrel.rmin - self.min_dist),  # type: ignore[func-returns-value]
                        endcap.lock("rmax"),
                    ),
                },
                {
                    "name": (
                        f"Option C: Increase rmin of endcap layer ({endcap.rmin}) to rmax of barrel layer"
                        f" ({barrel.rmax + self.min_dist})"
                    ),
                    "diff": abs(endcap.rmin - (barrel.rmax + self.min_dist)),
                    "locked": endcap.is_locked("rmin"),
                    "action": lambda barrel=barrel, endcap=endcap: (
                        setattr(endcap, "rmin", barrel.rmax + self.min_dist),  # type: ignore[func-returns-value]
                        endcap.lock("rmin"),
                    ),
                },
            ]

            # Filter out locked options which have already been modified by previous overlap resolutions
            available_options = [opt for opt in options if not opt["locked"]]

            # Choose the option with the lowest difference in values
            if available_options:
                best_option = min(available_options, key=lambda x: x["diff"])  # type: ignore[arg-type, return-value]
                print(f"Choosing {best_option['name']} with diff {best_option['diff']}\n")
                # Apply the best resolution option
                best_option["action"]()  # type: ignore[operator]
            else:
                raise Exception(
                    f"{mt.FAIL} Overlap resolution between thinned layer {cyl_a_name} and layer {cyl_b_name} not"
                    " possible. All possible options are locked. Manual check required."
                )

            # Update the thinned cylinder dictionary
            self.cylinders.thinned[cyl_a_name] = barrel if cyl_a.is_barrel else endcap
            self.cylinders.thinned[cyl_b_name] = barrel if cyl_b.is_barrel else endcap

            # Check again for overlapping layers
            n_overlaps, overlapping_layers = self.check_overlaps(cyl_type="thinned", print_output=False)

        print(f"{mt.SUCCESS} Thinned cylinder overlaps resolved.")

    def _symmetrize_cylinders(self, cyl_type: str = "thinned") -> dict[str, Cylinder]:
        # Get the dimensions for the requested cylinder type
        cyl_dict_pos_z = self._get_cylinder_dict(cyl_type)
        cyl_dict_neg_z = {}

        # Create the negative z cylinders from the positive halfspace
        for idx, cyl in cyl_dict_pos_z.items():
            if self.is_layer_continuous_in_z[idx]:
                cyl.zmin = 0

            neg_z_cyl = Cylinder(cyl.rmin, cyl.rmax, -cyl.zmax, -cyl.zmin, cyl.is_barrel)
            cyl_dict_neg_z[idx] = neg_z_cyl

        cyl_dict_pos_z = {str(idx) + "_POS": cyl for idx, cyl in sorted(cyl_dict_pos_z.items())}
        cyl_dict_neg_z = {str(idx) + "_NEG": cyl for idx, cyl in sorted(cyl_dict_neg_z.items())}

        return {**cyl_dict_pos_z, **cyl_dict_neg_z}

    def _merge_barrel(self) -> None:
        """
        Produce a single barrel layer by merging its positive and negative halves.
        """
        if not self.processed:
            raise Exception("Detector has not been processed yet. Process first with detector.process()")

        # merge positve and negative halves of barrel layers
        processed_cyl_names = [*self.cylinders.processed.keys()]
        for each_cyl_name in processed_cyl_names:
            if "_POS" in each_cyl_name and self.cylinders.processed[each_cyl_name].is_barrel:
                pos_cyl_name = each_cyl_name
                neg_cyl_name = each_cyl_name.replace("_POS", "_NEG")
                merged_cyc_name = each_cyl_name.replace("_POS", "")

                # ignore barrel layers which are not continuous at z=0
                if self.cylinders.processed[pos_cyl_name].zmin != 0 or self.cylinders.processed[neg_cyl_name].zmax != 0:
                    print(
                        f"{mt.WARNING} Barrel layer {merged_cyc_name} will not be merged. "
                        "Layer is not continuous at z=0."
                    )
                    continue

                self.cylinders.processed[pos_cyl_name].zmin = self.cylinders.processed[neg_cyl_name].zmin
                self.cylinders.processed[merged_cyc_name] = self.cylinders.processed[pos_cyl_name]
                del self.cylinders.processed[pos_cyl_name]
                del self.cylinders.processed[neg_cyl_name]

    def add_layer(self, layer: GeoLayer) -> None:
        # Ensure that the layer does not already exist in the simplified detector
        if layer.idx in self.cylinders.thinned:
            raise Exception(f"Layer {layer.idx} already exists in the simplified detector")

        # Add layer to the layer dictionary
        # Check if layer is continuous in z
        self.is_layer_continuous_in_z[layer.idx] = layer.is_continuous_in_z()
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
        # Merge barrel layers continuous at z=0
        self._merge_barrel()

    def check_overlaps(
        self,
        cyl_type: str = "thinned",
        print_output: bool = True,
        recursive: bool = False,
        coplanar: bool = False,
        debugIO: bool = False,
    ) -> tuple[int, list[list[str]]]:
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
