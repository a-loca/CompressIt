import numpy as np
import math


def build_dct_orthobasis(N):
    """
    Computes the Discrete Cosine Transform (DCT) orthonormal basis
    matrix of size N x N. This is done by sampling the cosine function
    at N equidistant points for each frequency k, where k ranges
    from 0 to N-1.

    Args:
        N (int): size of the required DCT matrix.

    Returns:
        D (numpy.ndarray): NxN matrix containing the orthonormal basis
                            vectors for DCT.
    """

    # Initializing matrix that will hold the orthonormal basis vectors
    D = np.empty((N, N))

    # Normalization vector to make each w_k an orthonormal base vector
    alpha = np.zeros(N)
    alpha[0] = N ** (-0.5)  # 1/√N
    alpha[1:] = N ** (-0.5) * math.sqrt(2)  # √2/√N

    # Looping through frequencies
    for k in range(N):
        # Sampling cosine at frequency k in N equidistant points and normalizing
        for i in range(N):
            D[k, i] = alpha[k] * math.cos(k * math.pi * (2 * i + 1) / (2 * N))

    return D


def dct_1D(f, D=None):
    """
    Computes the Discrete Cosine Transform (DCT) of a one variable function f,
    represented by a vector of its samples at N equidistant points.

    Args:
        f (numpy.ndarray): vector of samples of the function f.
        D (numpy.ndarray, optional): orthonormal basis for DCT transform.
                                      If not provided, it will be computed.

    Returns:
        c (numpy.ndarray): vector of DCT coefficients.
    """
    if D is None:
        # Computing orthonormal basis for DCP transform
        D = build_dct_orthobasis(len(f))
    # Dot product of each basis vector and function's samples vector
    c = D @ f
    return c


def idct_1D(c, D=None):
    """
    Computes the Inverse Discrete Cosine Transform (IDCT) of a
    vector of DCT coefficients c.

    Args:
        c (numpy.ndarray): vector of DCT coefficients.
        D (numpy.ndarray, optional): orthonormal basis for DCT transform.
                                      If not provided, it will be computed.
    Returns:
        f (numpy.ndarray): vector of N samples of the reconstructed function f,
                            where N is the length of c.
    """
    if D is None:
        D = build_dct_orthobasis(len(c))
    # Dot product of each basis vector and DCT coefficients vector
    f = D.T @ c
    return f
