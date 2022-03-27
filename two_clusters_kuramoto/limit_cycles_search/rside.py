from numba import njit
import numpy as np

class R_SIDES:

    @staticmethod
    @njit
    def coupled_pendulums_full(q, _, N, Mass, Alpha, Omega):
        X = np.empty(2 * N)
        n = 0
        while n < 2 * N: 
            X[n] = q[n + 1]
            X[n + 1] = 1 / Mass * (Omega + np.sum(np.sin(q[::2] - np.full(N, q[n]) - Alpha)) / N - q[n + 1])
            n += 2
        return X

    @staticmethod
    @njit
    def coupled_pendulums_rs(q, _, N, Mass, Alpha, K):
        X = np.empty(2)
        X[0] = q[1]
        X[1] = 1 / Mass * ( (N - 2 * K) / N * np.sin(Alpha) - \
            1 / N * ((N - K) * np.sin(q[0] + Alpha) + K * np.sin(q[0] - Alpha)) - q[1])
        return X

    @staticmethod
    @njit
    def coupled_pendulums_rs_linear_ksi(q, _, N, Mass, Alpha, K, DSomeRotMode_t):
        X = np.empty(2)
        X[0] = q[1]
        X[1] = - 1 / Mass * ( q[0] * ((N - K) / N * np.cos(DSomeRotMode_t[0] + Alpha) + \
            K / N * np.cos(Alpha)) + q[1])
        return X

    @staticmethod
    @njit
    def coupled_pendulums_rs_linear_eta(q, _, N, Mass, Alpha, K, DSomeRotMode_t):
        X = np.empty(2)
        X[0] = q[1]
        X[1] = - 1 / Mass * ( q[0] * ((N - K) / N * np.cos(Alpha) + \
            K / N * np.cos(DSomeRotMode_t[0] - Alpha)) + q[1])
        return X
