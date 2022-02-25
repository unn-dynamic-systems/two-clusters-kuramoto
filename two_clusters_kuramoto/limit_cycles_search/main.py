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
from existance_zones import M


def main():
    H_M = Config.H_M
    N, K, Alpha = Config.N, Config.K, Config.Alpha
    Mass_end = Config.Mass_end
    T0 = Config.T0
    IC0 = Config.IC0
    Mass = M(Alpha, K, N) + 2
    print(f'Initial Mass is {Mass}')

    assert IC0[0] == 0 # Main Convention

    IC, T = IC0, T0
    iteration = 0
    while Mass < Mass_end:
        args_orig = (N, Mass, Alpha, K)

        print("System args")
        print(args_orig)

        T, IC = limit_cycles.find_limit_cycle(R_SIDES.coupled_pendulums_rs, args_orig, IC, T,
                phase_period=2*mt.pi,
                eps=1e-5)

        print("Limit cycle initial condition")
        print(IC)
        print("Limit cycle time period")
        print(T)

        with open(f'{Config.data_storage}/{iteration}.pickle', 'wb') as f:
            pickle.dump(args_orig, f)
            pickle.dump(T, f); pickle.dump(IC, f)

        break

        Mass += H_M
        iteration += 1


if __name__ == "__main__":
    main()
    pass
