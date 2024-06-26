import matplotlib.pyplot as plt
from matplotlib.testing.compare import compare_images


def save_and_compare(name: str, refdir: str, testdir: str, tol: float = 0) -> bool:
    """
    Saves the current plot as an image and compares it with a reference image.

    Args:
        name (str): The name of the image file.
        refdir (str): The directory path where the reference image is located.
        testdir (str): The directory path where the test image will be saved.
        tol (float, optional): The tolerance value for image comparison. Defaults to 0.

    Returns:
        bool: True if the test image matches the reference image within the specified tolerance, False otherwise.
    """
    path_to_ref = f"{refdir}/{name}"
    path_to_test = f"{testdir}/{name}"

    plt.tight_layout()
    plt.savefig(path_to_test, dpi=300)

    return compare_images(path_to_ref, path_to_test, tol=tol) is None
