import numpy as np
import matplotlib.pyplot as plt
from utils import compute_base_matrix

plt.style.use(
    "https://github.com/dhaitz/matplotlib-stylesheets/raw/master/pitayasmoothie-light.mplstyle"
)


def dct_1D(f):
    """ """
    # Computing orthonormal basis for DCP transform
    D = compute_base_matrix(len(f))
    # Dot product of each basis vector and function's samples vector
    c = D @ f
    return c

def idct_1D(c):
    """
    """
    D = compute_base_matrix(len(c))
    # D.T is equal to D^-1 since D is orthogonal
    # c = D @ f -> f = D^-1 @ c = D.T @ c
    f = D.T @ c
    return f


def visualize_dct_1D(f, compression):
    # Sampling the function f at N equidistant points
    N = 100
    f_vect = np.empty(N)
    for i in range(N):
        f_vect[i] = f((2 * i + 1) / (2 * N))

    c = dct_1D(f_vect)

    plt.figure(figsize=(12, 6))

    # Plotting sampled function
    plt.subplot(2, 2, 1)
    plt.plot(f_vect)
    plt.title("Sampled function")

    # Plotting DCT coefficients
    plt.subplot(2, 2, 2)
    plt.bar(np.arange(N), c, width=1.0)
    plt.title("DCT coefficients")

    # Truncating coefficients
    c_trunc = c
    c_trunc[round(N * compression) :] = 0

    # Plotting truncated DCT coefficients
    plt.subplot(2, 2, 3)
    plt.bar(np.arange(N), c_trunc, width=1.0)
    plt.title(f"Truncated DCT coefficients at {compression*100}% compression")

    # Calculating IDCT
    f_trunc = idct_1D(c_trunc)

    # Plotting "compressed" function
    plt.subplot(2, 2, 4)
    plt.plot(f_trunc)
    plt.title("Compressed function")

    plt.show()


# Defining main function
def main():
    f = lambda x: 0 if x - 0.5 < 0 else 1
    # f = lambda x: 1
    visualize_dct_1D(f, 0.8)


if __name__ == "__main__":
    main()
