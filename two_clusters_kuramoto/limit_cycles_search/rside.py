from numba import njit
import numpy as np

class R_SIDES:
    @staticmethod
    @njit
    def coupled_pendulums_rs(q, _, N, Mass, Alpha, Omega):
        X = np.empty(2 * N)
        n = 0
        while n < 2 * N: 
            X[n] = q[n + 1]
            X[n + 1] = 1 / Mass * (Omega + np.sum(np.sin(q[::2] - np.full(N, q[n]) - Alpha)) / N - q[n + 1])
            n += 2
        return X

    @staticmethod
    @njit
    def coupled_pendulums_linear_rs(q, _, N, Mass, Alpha, phases_mode_t):
        X = np.empty(2 * N)
        n = 0
        while n < 2 * N: 
            X[n] = q[n + 1]
            X[n + 1] = 1 / Mass * (np.sum(np.cos(phases_mode_t - \
                np.full(N, phases_mode_t[int(n / 2)]) - Alpha) * (q[::2] - np.full(N, q[n]))) / N - q[n + 1])
            n += 2
        return X
