import numpy as np
from scipy.integrate import odeint
from scipy.signal import argrelextrema
from rside import R_SIDES

def find_initial_point(N, Mass, Alpha, K):
    ARGS = N, Mass, Alpha, K
    T, T_LAST = 2000, 600
    IC = np.array([0, 0.5])
    h = 1e-3; t = np.arange(0, T, h)
    frequencies = odeint(R_SIDES.coupled_pendulums_rs, IC, t, ARGS)[:, 1][- int(1 / h) * T_LAST:]
    [local_maxima_indexes] = argrelextrema(frequencies, np.greater)
    T = np.diff(t[local_maxima_indexes]).mean()
    IC = np.array([0, frequencies[local_maxima_indexes].mean()])
    print(IC, T)
    return IC, T

def main():
    N, Mass, Alpha, K = 9, 10, 1.57, 4
    find_initial_point(N, Mass, Alpha, K)

if __name__ == '__main__':
    main()
