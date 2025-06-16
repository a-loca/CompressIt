from scipy.fft import dct
from dct.dct2 import dct_2D
import numpy as np
import time
import matplotlib.pyplot as plt
import math

plt.style.use(
    "https://github.com/dhaitz/matplotlib-stylesheets/raw/master/pitayasmoothie-light.mplstyle"
)


def main():
    n_reps = 5
    cust_times = []
    lib_times = []
    cust_times_t = []  # should be O(N^3)
    lib_times_t = []  # should be O(N^2log(N))

    # test_sizes = [4, 8, 16, 24, 32, 48, 56, 64, 92, 128, 156, 192, 256]
    test_sizes = [2 + 8 * i for i in range(20)]
    print(test_sizes)

    np.random.seed(42)

    for i in range(len(test_sizes)):
        # Generate square matrices with increasing sizes
        # N = 2 ** (3 + i)
        N = test_sizes[i]

        print(f"Testing {N}x{N} matrix...")

        # Theoretical complexity
        lib_times_t.append(N**2 * math.log10(N))
        cust_times_t.append(N**3)

        # Generate random matrix of size N x N
        mat = np.random.rand(N, N)

        # Compute custom DCT
        print("\tCustom DCT...")
        mean = 0
        for j in range(n_reps):
            start = time.perf_counter()
            res = dct_2D(mat)
            end = time.perf_counter()
            elapsed = end - start
            mean += elapsed
            print(f"\t\tTest {j+1}: {elapsed:.6f}s")

        cust_times.append(mean / n_reps)

        # Compute fast DCT from library
        # Apply it two times, once on rows, obnce on cols
        print("\tScipy DCT...")
        mean = 0
        for j in range(n_reps):
            start = time.perf_counter()
            res2 = dct(dct(mat, norm="ortho", axis=1), norm="ortho", axis=0)
            end = time.perf_counter()
            elapsed = end - start
            mean += elapsed
            print(f"\t\tTest {j+1}: {elapsed:.6f}s")

        lib_times.append(mean / n_reps)

    # Plot result
    plt.figure(figsize=(12, 6))
    # plt.plot(test_sizes, cust_times, label="Custom DCT", marker="o")
    plt.plot(test_sizes, lib_times, label="Scipy DCT", marker="o")
    # plt.plot(
    #     test_sizes, cust_times_t, linestyle="dashed", label="Custom DCT complexity"
    # )
    # plt.plot(test_sizes, lib_times_t, linestyle="dashed", label="Scipy DCT complexity")
    plt.xlabel("Dimensione matrice N")
    plt.ylabel("Tempo (s)")
    plt.legend()
    # plt.yscale("log")

    plt.show()


if __name__ == "__main__":
    main()
