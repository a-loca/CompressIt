import matplotlib.pyplot as plt
import numpy as np
from dct.dct1D import dct_1D, idct_1D

def visualize_dct_1D(f, compression):
    plt.style.use(
        "https://github.com/dhaitz/matplotlib-stylesheets/raw/master/pitayasmoothie-light.mplstyle"
    )
    # Sampling the function f at N equidistant points
    N = 100
    x = (2 * np.arange(N) + 1) / (2 * N)
    f_vect = np.array([f(xi) for xi in x])

    c = dct_1D(f_vect)

    # Optional: thresholding small coefficients
    c[np.abs(c) < 1e-12] = 0

    plt.figure(figsize=(12, 6))

    # Plotting sampled function
    plt.subplot(2, 2, 1)
    plt.plot(x, f_vect)
    plt.title("Sampled function")
    plt.xlabel("x")
    plt.ylabel("f(x)")

    # Plotting DCT coefficients
    plt.subplot(2, 2, 2)
    plt.bar(np.arange(N), c, width=1.0)
    plt.title("DCT coefficients")
    plt.xlabel("Frequency (k)")
    plt.ylabel("Coefficient")

    # Truncating coefficients
    c_trunc = c.copy()
    c_trunc[round(N * compression) :] = 0

    # Plotting truncated DCT coefficients
    plt.subplot(2, 2, 3)
    plt.bar(np.arange(N), c_trunc, width=1.0)
    plt.title(f"Truncated DCT coefficients at {(1-compression)*100:.0f}% compression")
    plt.xlabel("Frequency (k)")
    plt.ylabel("Coefficient")

    # Calculating IDCT
    f_trunc = idct_1D(c_trunc)

    # Plotting "compressed" function
    plt.subplot(2, 2, 4)
    plt.plot(x, f_trunc)
    plt.title("Compressed function")
    plt.xlabel("x")
    plt.ylabel("f(x)")

    plt.tight_layout()
    plt.show()


def main():
    f = lambda x: 0 if x - 0.5 < 0 else 1
    # f = lambda x: 1
    visualize_dct_1D(f, 1)


if __name__ == "__main__":
    main()
