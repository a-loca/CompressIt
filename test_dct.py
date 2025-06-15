from scipy.fft import dct
from dct.dct2 import dct_2D
import numpy as np
import time
import matplotlib.pyplot as plt

plt.style.use(
    "https://github.com/dhaitz/matplotlib-stylesheets/raw/master/pitayasmoothie-light.mplstyle"
)

def main():
    n_tests = 5
    cust_times = []
    lib_times = []
    sizes = []
    
    np.random.seed(42)

    for i in range(n_tests):
        # Generate square matrices with increasing sizes
        N = 2 ** (3 + i)
        sizes.append(N)
        mat = np.random.rand(N, N)
        # Compute custom DCT
        start = time.perf_counter()
        res = dct_2D(mat)
        end = time.perf_counter()
        cust_times.append(end - start)

        # Compute fast DCT from library
        # Apply it two times, once on rows, once on cols
        start = time.perf_counter()
        res2 = dct(dct(mat, norm="ortho", axis=1), norm="ortho", axis=0)
        end = time.perf_counter()
        lib_times.append(end - start)

    # Plot result
    # TODO: Plot theoretical complexity of both functions
    plt.figure(figsize=(12, 6))
    plt.plot(sizes, cust_times, label="Custom DCT")
    plt.plot(sizes, lib_times, label="Scipy DCT")
    plt.xlabel("Dimensione matrice N")
    plt.ylabel("Tempo (s)")
    plt.legend()
    plt.yscale("log")
    plt.show()


if __name__ == "__main__":
    main()
