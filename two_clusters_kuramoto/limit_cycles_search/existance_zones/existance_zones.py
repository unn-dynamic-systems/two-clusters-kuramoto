import numpy as np
import math as mt
import seaborn as sns
import matplotlib.pyplot as plt
import pickle
from scipy.interpolate import interp1d

import os; cwd = os.path.dirname(os.path.abspath(__file__))
package_path = os.path.normpath(os.path.join(cwd, "..", "..", ".."))
import sys; sys.path.append(package_path)


def get_interpolate_function_from_file(filepath):
    with open(filepath, 'rb') as f:
        x = pickle.load(f)
        y = pickle.load(f)
        func = interp1d(x, y)
        return func

cwd = os.path.dirname(os.path.abspath(__file__))
tricommy_curve_inv = \
    get_interpolate_function_from_file(f'{cwd}/tricommy_curve_inv_{0}_to_{1}_h_{0.01}.pickle')

def M(Alpha, K, N):
    def R(K, N, Alpha):
        return np.sqrt( ((N - 2 * K) ** 2) * (np.sin(Alpha) ** 2) + (N ** 2) * (np.cos(Alpha) ** 2) )
    return N / R(K, N, Alpha) / tricommy_curve_inv((N - 2 * K) / R(K, N, Alpha) * np.absolute(np.sin(Alpha))) ** 2

def main():
    a_start, a_end = mt.pi / 6, 5 * mt.pi / 6
    a_h = 1e-3
    a_arr = np.linspace(a_start, a_end, int((a_end - a_start) / a_h))

    N, K = 5, 2
    m_arr = M(a_arr, K, N)
    sns.lineplot(x=a_arr, y=m_arr,label=f"N={N}, K={K}")

    N, K = 10, 4
    m_arr = M(a_arr, K, N)
    sns.lineplot(x=a_arr, y=m_arr,label=f"N={N}, K={K}", linestyle='--')

    N, K = 20, 7
    m_arr = M(a_arr, K, N)
    sns.lineplot(x=a_arr, y=m_arr,label=f"N={N}, K={K}", linestyle='--')

    N, K = 20, 3
    m_arr = M(a_arr, K, N)
    sns.lineplot(x=a_arr, y=m_arr,label=f"N={N}, K={K}", linestyle='--')

    N, K = 20, 1
    m_arr = M(a_arr, K, N)
    sns.lineplot(x=a_arr, y=m_arr,label=f"N={N}, K={K}", linestyle='--')

    plt.yscale('log')
    plt.savefig(f'ex_zones2.png')

if __name__ == '__main__':
    main()
