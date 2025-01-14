import pandas as pd

from pygeosimplify.simplify.cylinder import Cylinder
from pygeosimplify.simplify.helpers import r_overlap_filter, z_overlap_filter


def post_process_cylinders(  # noqa: C901
    cyl_dict: dict[str, Cylinder], cell_envelope: dict[str, Cylinder], min_dist: float = 1, envelope_width: float = 100
) -> tuple[dict[str, Cylinder], dict[str, Cylinder]]:
    # Convert cylinder dictionary to a dataframe
    df = pd.DataFrame.from_dict(cyl_dict, orient="index")
    # Add layer name as column
    df = df.rename_axis("cyl_name").reset_index()
    # Get the endcap and barrel layers
    endcap_layers = df[df.is_barrel.eq(False)]
    barrel_layers = df[df.is_barrel.eq(True)]

    # Fill gaps in r for endcap layers
    for idx, endcap_layer in endcap_layers.iterrows():
        limiting_layer_dict = {
            "out": get_cyl_limiting_r_extension(df, endcap_layer, side="OUT"),
            "in": get_cyl_limiting_r_extension(df, endcap_layer, side="IN"),
        }

        if limiting_layer_dict["out"] is None:
            # No layer limits the extension in r, so we extend it to the maximum r of the layers
            df.at[idx, "rmax"] = df.rmax.max()
        else:
            # Extend the radius of the endcap layer to the radius of the limiting layer
            df.at[idx, "rmax"] = limiting_layer_dict["out"].rmin - min_dist

        if limiting_layer_dict["in"] is None:
            # No layer limits the extension in r, so we extend it to the minimum r of the layers
            # This should usually correspond to the beam pipe, in principle could set this to 0, but this should be safer
            df.at[idx, "rmin"] = df.rmin.min()

    # Fill gaps in z for barrel layers
    for idx, barrel_layer in barrel_layers.iterrows():
        limiting_layer_dict = {
            "right": get_cyl_limiting_z_extension(df, barrel_layer, side="RIGHT"),
            "left": get_cyl_limiting_z_extension(df, barrel_layer, side="LEFT"),
        }

        if limiting_layer_dict["right"] is None:
            # No layer limits the extension in +z, so we extend it to the origin or the maximum z of the layers
            if "POS" in barrel_layer.cyl_name:
                df.at[idx, "zmax"] = df.zmax.max()
            if "NEG" in barrel_layer.cyl_name:
                df.at[idx, "zmax"] = 0
        else:
            # Extend the z of the barrel layer to the z of the limiting layer
            df.at[idx, "zmax"] = limiting_layer_dict["right"].zmin - min_dist

        if limiting_layer_dict["left"] is None:
            # No layer limits the extension in -z, so we extend it to the origin or the minimum z of the layers
            if "POS" in barrel_layer.cyl_name:
                df.at[idx, "zmin"] = 0
            if "NEG" in barrel_layer.cyl_name:
                df.at[idx, "zmin"] = df.zmin.min()
        else:
            # Extend the z of the barrel layer to the z of the limiting layer
            df.at[idx, "zmin"] = limiting_layer_dict["left"].zmax + min_dist

    # Grow barrel layers in z to the z of the limiting endcap layer
    for idx, barrel_layer in barrel_layers.iterrows():
        limiting_layer_dict = {
            "out": get_cyl_limiting_r_extension(df, barrel_layer, side="OUT"),
            "in": get_cyl_limiting_r_extension(df, barrel_layer, side="IN"),
        }

        if limiting_layer_dict["out"] is None:
            df.at[idx, "rmax"] = cyl_dict[barrel_layer.cyl_name].rmax
        else:
            # Grow rmax to the radius of the limiting layer (but not larger than the radius of the cell envelope)
            r_lim = limiting_layer_dict["out"].rmin
            if r_lim > cell_envelope[barrel_layer.cyl_name].rmax:
                df.at[idx, "rmax"] = cell_envelope[barrel_layer.cyl_name].rmax
            else:
                df.at[idx, "rmax"] = r_lim - min_dist

        if limiting_layer_dict["in"] is None:
            df.at[idx, "rmin"] = cyl_dict[barrel_layer.cyl_name].rmin
        else:
            # Reduce rmin to the radius of the limiting layer (but not smaller than the radius of the cell envelope)
            r_lim = limiting_layer_dict["in"].rmax
            if r_lim < cell_envelope[barrel_layer.cyl_name].rmin:
                df.at[idx, "rmin"] = cell_envelope[barrel_layer.cyl_name].rmin
            else:
                df.at[idx, "rmin"] = r_lim + min_dist

    # Grow endcap layers to the z of the limiting layers
    for idx, endcap_layer in endcap_layers.iterrows():
        limiting_layer_dict = {
            "right": get_cyl_limiting_z_extension(df, endcap_layer, side="RIGHT"),
            "left": get_cyl_limiting_z_extension(df, endcap_layer, side="LEFT"),
        }

        if limiting_layer_dict["right"] is None:
            df.at[idx, "zmax"] = cyl_dict[endcap_layer.cyl_name].zmax
        else:
            # Grow zmax to the z of the limiting layer (but not larger than the cell envelope z)
            z_lim = limiting_layer_dict["right"].zmin
            if z_lim > cell_envelope[endcap_layer.cyl_name].zmax:
                df.at[idx, "zmax"] = cell_envelope[endcap_layer.cyl_name].zmax
            else:
                df.at[idx, "zmax"] = z_lim - min_dist

        if limiting_layer_dict["left"] is None:
            df.at[idx, "zmin"] = cyl_dict[endcap_layer.cyl_name].zmin
        else:
            # Reduce zmin to the z of the limiting layer  (but not smaller than the cell envelope z)
            z_lim = limiting_layer_dict["left"].zmax
            if z_lim < cell_envelope[endcap_layer.cyl_name].zmin:
                df.at[idx, "zmin"] = cell_envelope[endcap_layer.cyl_name].zmin
            else:
                df.at[idx, "zmin"] = z_lim + min_dist

    # Convert back to dictionary
    cyl_dict_out = df.set_index("cyl_name").to_dict("index")

    # Convert back to Cylinder objects
    cyl_dict = {
        cyl_name: Cylinder(
            cyl_dict_out[cyl_name]["rmin"],
            cyl_dict_out[cyl_name]["rmax"],
            cyl_dict_out[cyl_name]["zmin"],
            cyl_dict_out[cyl_name]["zmax"],
            cyl_dict_out[cyl_name]["is_barrel"],
        )
        for cyl_name in cyl_dict_out
    }

    # Finally get a cylinder envelope around all layers
    cyl_envelope_dict = get_cylinder_envelope(df, min_dist=min_dist, envelope_width=envelope_width)

    return cyl_dict, cyl_envelope_dict


def get_cylinder_envelope(df: pd.DataFrame, min_dist: float, envelope_width: float) -> dict[str, Cylinder]:
    """! Adds an envelope cylinder around the whole detector to the registry"""
    max_z = df.zmax.max()
    min_z = df.zmin.min()
    max_r = df.rmax.max()

    envelope_dict = {}

    envelope_dict["BarrelEnvelope"] = Cylinder(max_r + min_dist, max_r + envelope_width, min_z, max_z, True)
    envelope_dict["EndcapEnvelopePos"] = Cylinder(
        0, max_r + min_dist + envelope_width, max_z + min_dist, max_z + min_dist + envelope_width, False
    )
    envelope_dict["EndcapEnvelopeNeg"] = Cylinder(
        0, max_r + min_dist + envelope_width, min_z - min_dist - envelope_width, min_z - min_dist, False
    )

    return envelope_dict


def get_cyl_limiting_r_extension(df: pd.DataFrame, layer: pd.DataFrame, side: str = "OUT") -> Cylinder | None:
    if side not in ["OUT", "IN"]:
        raise ValueError("side must be either OUT or IN")

    # Positive or negative halfspace (in z) where the layer is located
    z_half_space = "POS" if "POS" in layer.cyl_name else "NEG"

    # Consider only layers on the side of the considered endcap layer
    side_sel = df.cyl_name.str.contains("POS") if z_half_space == "POS" else df.cyl_name.str.contains("NEG")

    # Consider only (barrel and endcap) layer candidates that could overlap in z when extending r of the layer
    z_overlap_sel = df.apply(z_overlap_filter, args=(layer.zmin, layer.zmax), axis=1) & df.cyl_name.ne(layer.cyl_name)

    r_sel = df.rmin > layer.rmax if side == "OUT" else df.rmax < layer.rmin

    # The (barrel and endcap) layer candidates that would overlap in case of an infinte r extension
    cyl_candidates = df.loc[z_overlap_sel & r_sel & side_sel]

    # No candidates -> the extension of the endcap layer in r towards the chosen endcap side (out or in) is not limited
    if cyl_candidates.empty:
        return None

    # The one with the smallest (largest) rmin (rmax) is the limiting endcap layer for out (in) side of layer
    limiting_cyl_idx = cyl_candidates["rmin"].idxmin() if side == "OUT" else cyl_candidates["rmax"].idxmax()

    limiting_cyl_df = cyl_candidates.loc[limiting_cyl_idx]

    limiting_cyl = Cylinder(
        limiting_cyl_df.rmin,
        limiting_cyl_df.rmax,
        limiting_cyl_df.zmin,
        limiting_cyl_df.zmax,
        limiting_cyl_df.is_barrel,
    )

    return limiting_cyl


def get_cyl_limiting_z_extension(df: pd.DataFrame, layer: pd.DataFrame, side: str = "RIGHT") -> Cylinder | None:
    if side not in ["RIGHT", "LEFT"]:
        raise ValueError("side must be either RIGHT or LEFT")

    # Positive or negative halfspace (in z) where the layer is located
    z_half_space = "POS" if "POS" in layer.cyl_name else "NEG"

    # Consider only layers on the side of the considered endcap layer
    side_sel = df.cyl_name.str.contains("POS") if z_half_space == "POS" else df.cyl_name.str.contains("NEG")

    # Consider only (barrel and endcap) layer candidates that could overlap in z when extending r of the layer
    r_overlap_sel = df.apply(r_overlap_filter, args=(layer.rmin, layer.rmax), axis=1) & df.cyl_name.ne(layer.cyl_name)

    z_sel = df.zmin > layer.zmax if side == "RIGHT" else df.zmax < layer.zmin

    # The (barrel and endcap) layer candidates that would overlap in case of an infinte r extension
    cyl_candidates = df.loc[r_overlap_sel & z_sel & side_sel]

    # No candidates -> the extension of the endcap layer in r towards the chosen endcap side (out or in) is not limited
    if cyl_candidates.empty:
        return None

    # The one with the smallest (largest) zmin (zmax) is the limiting endcap layer for right (left) side of layer
    limiting_cyl_idx = cyl_candidates["zmin"].idxmin() if side == "RIGHT" else cyl_candidates["zmax"].idxmax()

    limiting_cyl_df = cyl_candidates.loc[limiting_cyl_idx]

    limiting_cyl = Cylinder(
        limiting_cyl_df.rmin,
        limiting_cyl_df.rmax,
        limiting_cyl_df.zmin,
        limiting_cyl_df.zmax,
        limiting_cyl_df.is_barrel,
    )

    return limiting_cyl
