from .dct1 import dct_1D, idct_1D
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np


def dct_2D(f):
    """
    Computes the Discrete Cosine Transform (DCT) of a 2D matrix representing 
    the sampled values of a function in two variables. It is computed by applying
    the DCT 1D to each column and each row of the matrix.
    
    Args:
        f (np.ndarray): A 2D numpy array representing the sampled values of a function.
    
    Returns:
        np.ndarray: A 2D numpy array containing the DCT coefficients.
    """
    c = f.copy()
    N = f.shape[0]
    # DCT_1D for each column
    for i in range(N):
        c[:, i] = dct_1D(c[:, i])

    # DCT_1D for each row
    for i in range(N):
        c[i, :] = dct_1D(c[i, :])
    return c


def idct_2D(c):
    
    f = c.copy()
    N = f.shape[0]

    # IDCT_1D for each column
    for i in range(N):
        f[:, i] = idct_1D(f[:, i])

    # IDCT_1D for each row
    for i in range(N):
        f[i, :] = idct_1D(f[i, :])

    return f


def visualize_dct_2D(f, compression):
    plt.style.use(
        "https://github.com/dhaitz/matplotlib-stylesheets/raw/master/pitayasmoothie-light.mplstyle"
    )

    # Sampling the function f at N equidistant points
    N = 10
    f_mat = np.empty((N, N))

    # Sampling function in 2 variables
    for i in range(N):
        for j in range(N):
            f_mat[i, j] = f((2 * i + 1) / (2 * N), (2 * j + 1) / (2 * N))

    # Computing DCT for 2D matrix
    c = dct_2D(f_mat)

    # Set up the figure and Axes
    fig = plt.figure(figsize=(14, 6))
    ax1 = fig.add_subplot(221, projection="3d")
    ax2 = fig.add_subplot(222, projection="3d")
    ax3 = fig.add_subplot(223, projection="3d")
    ax4 = fig.add_subplot(224, projection="3d")

    # Sampled 2D function
    for i in range(N):
        for j in range(N):
            ax1.bar3d(i, j, 0, 0.9, 0.9, f_mat[i][j])

    ax1.set_title("Sampled Function")

    # DCT coefficients
    for i in range(N):
        for j in range(N):
            ax2.bar3d(i, j, 0, 0.9, 0.9, c[i][j])

    ax2.set_title("DCT coefficients")

    # Truncated DCT coefficients
    c_trunc = c.copy()
    c_trunc[round(N * compression) :, :] = 0
    c_trunc[:, round(N * compression) :] = 0

    # Truncated DCT coefficients
    for i in range(N):
        for j in range(N):
            ax3.bar3d(i, j, 0, 0.9, 0.9, c_trunc[i][j])

    ax3.set_title("Truncated DCT coefficients")

    # Compressed 2D function
    f_trunc = idct_2D(c_trunc)

    for i in range(N):
        for j in range(N):
            ax4.bar3d(i, j, 0, 0.9, 0.9, f_trunc[i][j])

    ax4.set_title("Compressed function")

    plt.tight_layout()
    plt.show()


# Defining main function
def main():
    # f = lambda x, y: 1
    sign = lambda x: 0 if x - 0.5 < 0 else 1
    f = lambda x, y: sign(x) * sign(y)
    visualize_dct_2D(f, 0.5)


if __name__ == "__main__":
    main()
