import numpy as np
import matplotlib.pyplot as plt
from dct.dct2D import dct_2D, idct_2D

def visualize_dct_2D(f, compression):
    plt.style.use(
        "https://github.com/dhaitz/matplotlib-stylesheets/raw/master/pitayasmoothie-light.mplstyle"
    )

    # Sampling the function f at N equidistant points
    N = 10
    f_mat = np.empty((N, N))
    x_vals = (2 * np.arange(N) + 1) / (2 * N)

    # Sampling function in 2 variables
    for i in range(N):
        for j in range(N):
            f_mat[i, j] = f(x_vals[i], x_vals[j])

    # Computing DCT for 2D matrix
    c = dct_2D(f_mat)
    # Optional: set small coefficients to zero
    c[np.abs(c) < 1e-12] = 0

    # Set up the figure and Axes
    fig = plt.figure(figsize=(12, 12))
    ax1 = fig.add_subplot(221, projection="3d")
    ax2 = fig.add_subplot(222, projection="3d")
    ax3 = fig.add_subplot(223, projection="3d")
    ax4 = fig.add_subplot(224, projection="3d")

    # Sampled 2D function
    for i in range(N):
        for j in range(N):
            x = x_vals[i]
            y = x_vals[j]
            z = f_mat[i, j]
            ax1.bar3d(x, y, 0, 0.9 / N, 0.9 / N, z)

    ax1.set_title("Sampled Function")
    ax1.set_xlabel("x")
    ax1.set_ylabel("y")
    ax1.set_zlabel("f(x, y)")

    # DCT coefficients
    for i in range(N):
        for j in range(N):
            ax2.bar3d(i, j, 0, 0.9, 0.9, c[i][j])

    ax2.set_title("DCT coefficients")
    ax2.set_xlabel("Frequency x")
    ax2.set_ylabel("Frequency y")
    ax2.set_zlabel("Coefficient")

    # Truncated DCT coefficients
    c_trunc = c.copy()
    c_trunc[round(N * compression) :, :] = 0
    c_trunc[:, round(N * compression) :] = 0

    # Truncated DCT coefficients
    for i in range(N):
        for j in range(N):
            ax3.bar3d(i, j, 0, 0.9, 0.9, c_trunc[i][j])

    ax3.set_title(
        f"Truncated DCT coefficients at {(1-compression)*100:.0f}% compression"
    )
    ax3.set_xlabel("Frequency x")
    ax3.set_ylabel("Frequency y")
    ax3.set_zlabel("Coefficient")

    # Compressed 2D function
    f_trunc = idct_2D(c_trunc)

    for i in range(N):
        for j in range(N):
            x = x_vals[i]
            y = x_vals[j]
            z = f_trunc[i, j]
            ax4.bar3d(x, y, 0, 0.9 / N, 0.9 / N, z)

    ax4.set_title("Compressed function")
    ax4.set_xlabel("x")
    ax4.set_ylabel("y")
    ax4.set_zlabel("f(x, y)")

    plt.tight_layout()
    plt.show()


# Defining main function
def main():
    # f = lambda x, y: 1
    sign = lambda x: 0 if x - 0.5 < 0 else 1
    f = lambda x, y: sign(x) * sign(y)
    visualize_dct_2D(f, 1)


if __name__ == "__main__":
    main()
