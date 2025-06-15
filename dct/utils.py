import numpy as np
import math

def compute_base_matrix(N):
    """
    Computes the Discrete Cosine Transform (DCT) orthonormal basis matrix of size N x N.
    """

    # Initializing matrix that will hold the basis vectors
    D = np.empty((N, N))

    # Normalization vector to make each w_k an orthonormal base vector
    alpha = np.zeros(N)
    alpha[0] = N ** (-0.5)  # 1/√N
    alpha[1:] = N ** (-0.5) * math.sqrt(2)  # √2/√N

    # Looping through frequencies
    for k in range(N):
        # Sampling cosine at frequency k in N equidistant points
        for i in range(N):
            D[k, i] = alpha[k] * math.cos(k * math.pi * (2 * i + 1) / (2 * N))

    return D
