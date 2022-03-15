import pickle
import math as mt
from rside import R_SIDES
from numpy.linalg import eig as get_eigenvalues

# Remove it if you are installed our module already
import os; cwd = os.path.dirname(os.path.abspath(__file__))
package_path = os.path.normpath(os.path.join(cwd, "..", "..", ".."))
import sys; sys.path.append(package_path)

# Every import of our library should looks like this
from calculation import limit_cycles


def dump(data, filename):
    with open(f'{filename}', 'ab') as f:
        pickle.dump(data, f)

def calcline_limit_cycle(params, param_politics, filename_for_dump):
    IC, T, *args_orig = params
    args_orig = tuple(args_orig)
    assert IC[0] == 0 # Main Convention

    while True:
        while True:
            try:
                T, IC = limit_cycles.find_limit_cycle(R_SIDES.coupled_pendulums_rs, args_orig, IC, T,
                    phase_period=2*mt.pi,
                    eps=1e-5)
                break
            except ArithmeticError:
                is_continue, args_orig = param_politics.update(*args_orig, fail=True)
                if not is_continue: return

        d = {"system args": args_orig, "Limit Cycle Period": T, "Initial Conditions": IC}
        dump(d, filename_for_dump)

        is_continue, args_orig = param_politics.update(*args_orig, fail=False)
        if not is_continue: return

def calcline_stability(filename_for_get_data, filename_for_dump):
    with open(filename_for_get_data, 'rb') as f:
        while True:
            try:
                d = pickle.load(f)
                args_orig = d.get("system args")
                T = d.get("Limit Cycle Period")
                IC = d.get("Initial Conditions")

                M_eta = limit_cycles.get_monogrommy_matrix(R_SIDES.coupled_pendulums_rs,
                                            R_SIDES.coupled_pendulums_rs_linear_eta,
                                            IC, T,
                                            args_orig, args_orig)

                M_ksi = limit_cycles.get_monogrommy_matrix(R_SIDES.coupled_pendulums_rs,
                                            R_SIDES.coupled_pendulums_rs_linear_ksi,
                                            IC, T,
                                            args_orig, args_orig)

                eta_eig, _  = get_eigenvalues(M_eta)
                ksi_eig, _ = get_eigenvalues(M_ksi)

                d = {"system args": args_orig,"Limit Cycle Period": T, "Initial Conditions": IC,
                    "eta_eig": eta_eig, "ksi_eig": ksi_eig}

                dump(d, filename_for_dump)

            except EOFError:
                break
