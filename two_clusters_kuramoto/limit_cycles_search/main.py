import numpy as np
import math as mt
import pickle
from numpy.linalg import eig as get_eigen_vaues_from_M

# Remove it if you are installed our module already
import os; cwd = os.path.dirname(os.path.abspath(__file__))
package_path = os.path.normpath(os.path.join(cwd, "..", "..", ".."))
import sys; sys.path.append(package_path)

from rside import R_SIDES
from config import Config

# Every import of our library should looks like this
from calculation import limit_cycles

def main():
    H_M = Config.H_M
    N, Mass, Alpha, Omega = Config.N, Config.Mass, Config.Alpha, Config.Omega
    T0 = Config.T0
    IC0 = Config.IC0

    assert IC0[0] == 0 # Main Convention

    IC, T = IC0, T0
    iteration = 0
    while True:
        args_orig = (N, Mass, Alpha, Omega)
        args_linear = (N, Mass, Alpha)

        print("System args")
        print(args_orig)

        T, IC = limit_cycles.find_limit_cycle(R_SIDES.coupled_pendulums_rs, args_orig, IC, T, phase_period=2 * mt.pi)

        print("Limit cycle initial condition")
        print(IC)
        print("Limit cycle period")
        print(T)

        M = limit_cycles.get_monogrommy_matrix(R_SIDES.coupled_pendulums_rs,
                                               R_SIDES.coupled_pendulums_linear_rs,
                                               IC, T,
                                               args_linear, args_orig)

        E, _ = get_eigen_vaues_from_M(M)
        print("Eigen values of monogrommy matrix")
        print(E)

        with open(f'{Config.data_storage}/{iteration}.pickle', 'wb') as f:
            pickle.dump(args_orig, f)
            pickle.dump(T, f); pickle.dump(IC, f)
            pickle.dump(M, f); pickle.dump(E, f)

        Mass += H_M
        iteration += 1
        if iteration == 10:
            break


if __name__ == "__main__":
    main()
