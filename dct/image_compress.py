import numpy as np
import math
from scipy.fft import dct, idct
from PIL import Image


def _subdivide_image(pixels, f):
    """
    Subdivides an image into F x F blocks represented as matrices of pixel values.

    Args:
        pixels (np.ndarray): 2D array of pixel values representing the image.
        f (int): size of the blocks to subdivide the image into.

    Returns:
        blocks (list): list of 2D arrays representing the F x F blocks
                        of the image. The blocks are ordered row-wise.
        n_rows (int): number of rows of blocks contained in the image.
                        Corresponds to the number of the number of F x F
                        blocks that fit in the image vertically.
        n_cols (int): number of columns of blocks contained in the image.
                        Corresponds to the number of F x F blocks that fit
                        in the image horizontally.
    """

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
    """
    Rebuilds an image starting from a list of F x F blocks. It does so by stacking
    the blocks horizontally based on the number of blocks in each row, and then
    stacking the resulting rows vertically.

    Args:
        blocks (list): list of 2D arrays representing the F x F blocks of the image.
        n_rows (int): number of rows of blocks contained in the image.
                        Corresponds to the number of the number of F x F
                        blocks that fit in the image vertically.
        n_cols (int): number of columns of blocks contained in the image.
                        Corresponds to the number of F x F blocks that fit
                        in the image horizontally.
    Returns:
        image (np.ndarray): 2D array of pixel values representing the original image.
    """

    rows = []

    for i in range(n_rows):
        # Build image row by row through concatenation of cols
        rows.append(np.hstack(blocks[i * n_cols : (i + 1) * n_cols]))

    # Stack rows to build image
    image = np.vstack(rows)

    return image


def jpg_compression(image, f, d):
    """
    Compresses a specified image using a version of the JPEG compression
    algorithm without quantization matrix. Works on square images.
    The algorithm consists of the following steps:
    1. Subdivide the image into F x F blocks.
    2. For each block:
        1. Apply the Discrete Cosine Transform (DCT) to each block,
        2. Zero out all values of the resulting DCT coefficients matrix
            that are to the right of the d-th diagonal, meaning that
            all coefficients with indices (i, j) where i +j >= d are zeroed.
        3. Apply the Inverse Discrete Cosine Transform (IDCT) to the modified
            coefficients.
        4. Round all resulting pixel values to the nearest integer and clip
            them to the range [0, 255].
    3. Rebuild the original image by stacking the blocks in the correct order.

    Args:
        image (PIL.Image): the image to be compressed to JPEG format.
        F (int): size of the blocks to subdivide the image into.
        d (int): parameter that determines how many coefficients to keep,
                    deciding how much compression will be applied to the image.

    Returns:
        compressed_image (PIL.Image): the compressed image in JPEG format.
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
