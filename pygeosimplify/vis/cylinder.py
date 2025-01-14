import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from scipy.linalg import norm

from pygeosimplify.simplify.cylinder import Cylinder


def get_normals(v: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Get two vectors that form a basis w/ v.

    Note: returned vectors are unit
    """
    not_v = np.array([1, 0, 0])
    if np.all(np.abs(v) == not_v):
        not_v = np.array([0, 1, 0])
    n1 = np.cross(v, not_v)
    n1 /= norm(n1)
    n2 = np.cross(v, n1)
    return n1, n2


def generate_cylinder_face_points(
    start: np.ndarray, end: np.ndarray, start_radius: float, end_radius: float, linspace_count: int = 300
) -> np.ndarray:
    """Generate a 3d mesh of a cylinder with start and end points, and varying radius."""
    v = end - start
    length = norm(v)
    v = v / length
    n1, n2 = get_normals(v)

    length_values, theta = np.meshgrid(
        np.linspace(0, length, linspace_count), np.linspace(0, 2 * np.pi, linspace_count)
    )

    radii = np.linspace(start_radius, end_radius, linspace_count)
    rsin = np.multiply(radii, np.sin(theta))
    rcos = np.multiply(radii, np.cos(theta))

    return np.array([start[i] + v[i] * length_values + n1[i] * rsin + n2[i] * rcos for i in range(3)])


def generate_cylinder_endcap_points(rmin: float, rmax: float, z: float, linspace_count: int = 300) -> tuple:
    # Create an array of angles
    theta = np.linspace(0, 2 * np.pi, linspace_count)
    # Create an array of radii in the specified range
    radii = np.linspace(rmin, rmax, linspace_count)

    # Create a grid of points in polar coordinates
    theta, radii = np.meshgrid(theta, radii)

    # Convert polar coordinates to Cartesian coordinates
    x = radii * np.cos(theta)
    y = radii * np.sin(theta)
    z = np.full_like(y, z)  # Z coordinate remains constant

    return x, y, z


def plot_cylinder(
    cylinder: Cylinder,
    ax: Axes3D = None,
    color: tuple[float, float, float] | str = "black",
    alpha: float = 0.2,
    linspace_count: int = 300,
) -> Axes3D:
    if ax is None:
        fig = plt.figure()
        ax = fig.add_subplot(111, projection="3d")

    ax.grid(False)
    ax.xaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
    ax.yaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
    ax.zaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))

    """Plot a 3d cylinder."""
    if cylinder.rmin >= cylinder.rmax:
        raise Exception("Cylinder rmin must be less than rmax")
    if cylinder.zmin >= cylinder.zmax:
        raise Exception("Cylinder zmin must be less than zmax")

    # For the endcaps only translation in z is supported and not rotation
    startPos = np.array([0, 0, cylinder.zmin])
    endPos = np.array([0, 0, cylinder.zmax])

    # Plot the cylinder face
    x, y, z = generate_cylinder_face_points(
        startPos, endPos, cylinder.rmax, cylinder.rmax, linspace_count=linspace_count
    )
    ax.plot_surface(x, y, z, color=color, alpha=alpha)
    # Plot the cylinder endcaps
    for zValue in [startPos[2], endPos[2]]:
        x, y, z = generate_cylinder_endcap_points(cylinder.rmin, cylinder.rmax, zValue, linspace_count=linspace_count)
        ax.plot_surface(x, y, z, color=color, alpha=alpha)

    return ax
