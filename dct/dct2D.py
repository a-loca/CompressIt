from .dct1D import dct_1D, idct_1D, build_dct_orthobasis


def dct_2D(f):
    """
    Computes the Discrete Cosine Transform (DCT) of a 2D matrix representing
    the sampled values of a function in two variables. It is done by applying
    the DCT 1D to each column and each row of the matrix.

    Args:
        f (np.ndarray): A 2D numpy array representing the sampled values of a function.

    Returns:
        np.ndarray: A 2D numpy array containing the DCT coefficients.
    """
    c = f.copy()
    N = f.shape[0]

    # Precompute the orthonormal basis for efficiency
    D = build_dct_orthobasis(N)

    # DCT_1D for each column
    for i in range(N):
        c[:, i] = dct_1D(c[:, i], D)

    # DCT_1D for each row
    for i in range(N):
        c[i, :] = dct_1D(c[i, :], D)
    return c


def idct_2D(c):
    """
    Computes the Inverse Discrete Cosine Transform (IDCT) of a 2D matrix representing
    the DCT coefficients of a function in two variables. It is done by appling the
    IDCT 1D to each column and each row of the coefficients matrix.

    Args:
        c (np.ndarray): A 2D numpy array containing the DCT coefficients.

    Returns:
        np.ndarray: A 2D numpy array representing the reconstructed function.
    """

    f = c.copy()
    N = f.shape[0]

    # Precompute orthonormal basis for efficiency
    D = build_dct_orthobasis(N)

    # IDCT_1D for each column
    for i in range(N):
        f[:, i] = idct_1D(f[:, i], D)

    # IDCT_1D for each row
    for i in range(N):
        f[i, :] = idct_1D(f[i, :], D)

    return f
