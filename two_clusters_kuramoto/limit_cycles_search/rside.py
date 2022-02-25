from numba import njit
import numpy as np

class R_SIDES:
    @staticmethod
    @njit
    def coupled_pendulums_rs(q, _, N, Mass, Alpha, K):
        X = np.empty(2)
        X[0] = q[1]
        X[1] = 1 / Mass * ( (N - 2 * K) / N * np.sin(Alpha) - 1 / N * ((N - K) * np.sin(q[0] + Alpha) + K * np.sin(q[0] - Alpha)) - q[1])
        return X

