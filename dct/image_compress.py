import numpy as np
import math
from scipy.fft import dct, idct
from PIL import Image


def _subdivide_image(pixels, f):
    height, width = pixels.shape

    # Array of matrices representing each block
    blocks = []

    # Getting number of rows of blocks in the image
    n_rows = math.floor(height / f)

    # Getting number of columns of blocks in the image
    n_cols = math.floor(width / f)

    # Looping through rows
    for i in range(n_rows):
        # Looping through columns
        for j in range(n_cols):
            block = pixels[i * f : (i + 1) * f, j * f : (j + 1) * f]
            blocks.append(block)

    return blocks, n_rows, n_cols


def _rebuild_image(blocks, n_rows, n_cols):

    rows = []

    for i in range(n_rows):
        # Build image row by row through concatenation of cols
        rows.append(np.hstack(blocks[i * n_cols : (i + 1) * n_cols]))

    # Stack rows to build image
    image = np.vstack(rows)

    return image


def jpg_compression(image, f, d):
    """
    Images are square

    Steps:

    Args:

    Returns:
    """

    # Get pixel values as a numpy matrix
    pixels = np.asarray(image)

    # Subdividing image in FxF blocks
    blocks, n_rows, n_cols = _subdivide_image(pixels, f)

    compressed_blocks = []

    # Apply DCT to every block
    for block in blocks:

        # 1. Apply DCT to block: 1D DCT to columns, then rows
        coeff = dct(dct(block, norm="ortho", axis=1), norm="ortho", axis=0)

        # 2. Cut values to the right of d-th diagonal
        for i in range(f):
            for j in range(f):
                if i + j >= d:
                    coeff[i, j] = 0

        # 3. Apply IDCT: 1D IDCT to columns, then rows
        compressed_block = idct(idct(coeff, norm="ortho", axis=1), norm="ortho", axis=0)

        # 4. Round values, then range [0, 255]
        #   np.rint: rounds elements to nearest integer
        #   np.clip: sets elements < min to min and elements > max to max
        compressed_block = np.clip(np.rint(compressed_block), 0, 255).astype(np.uint8)

        compressed_blocks.append(compressed_block)

    # Rebuild original image by stacking blocks horizontally and vertically
    compressed_image = Image.fromarray(
        _rebuild_image(compressed_blocks, n_cols=n_cols, n_rows=n_rows)
    )

    return compressed_image
