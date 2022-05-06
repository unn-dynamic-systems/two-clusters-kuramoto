import pickle
import math as mt
import numpy as np
from rside import R_SIDES
from numpy.linalg import eig as get_eigenvalues
from scipy.integrate import odeint

# Remove it if you are installed our module already
import os; cwd = os.path.dirname(os.path.abspath(__file__))
package_path = os.path.normpath(os.path.join(cwd, "..", "..", "..", "calculation"))
import sys; sys.path.append(package_path)

# Every import of our library should looks like this
from unn_ds import limit_cycles
from unn_ds import integrators


def dump(data, filename):
    with open(f'{filename}', 'ab') as f:
        pickle.dump(data, f)

def get_state_special(last_state):
    last_state = last_state.copy()
    last_state[0] = 0
    eps = 1e-5
    short_res = []
    res = "|"
    N = mt.floor(len(last_state) / 2)
    values = []
    for i in range(N):
        values.append(
            (
                last_state[2 * i + 1],
                i + 1,
            )
        )
    values_np = np.array(
        values,
        dtype=[
            ("phase", float),
            ("index", int),
        ],
    )
    sort_values = np.sort(values_np, kind="mergesort", order="phase")
    i = 1
    while i < N:
        chunk = []
        while i < N and mt.fabs(sort_values[i][0] - sort_values[i - 1][0]) < eps:
            chunk.append("{}".format(sort_values[i - 1][1]))
            i += 1
        chunk.append("{}".format(sort_values[i - 1][1]))
        short_res.append(str(len(chunk)))
        chunk.sort(key=lambda s_i: int(s_i))
        res += "=".join(chunk) + "|"
        i += 1
    if i == N:
        res += "{}|".format(sort_values[i - 1][1])
        short_res.append("1")
    short_res.sort()
    res += " ~ " + ":".join(short_res)
    return res

def calcline_stats(params, param_politics, filename_for_dump):
    T_END, ITERATIONS, *system_args = params
    system_args = tuple(system_args)
    N, _, _, _ = system_args

    while True:
        states = []
        for _ in range(ITERATIONS):
            IC = np.random.random(2 * N)
            h = 1e-3; t = np.arange(0, T_END, h)
            last_state = odeint(R_SIDES.coupled_pendulums_full, IC, t, system_args)[-1]
            # last_state = integrators.RK4(R_SIDES.coupled_pendulums_full, IC, 0, T_END, system_args)
            state = get_state_special(last_state)
            states.append(state)

        d = {"system args": system_args, "states": states}
        dump(d, filename_for_dump)

        is_continue, system_args = param_politics.update(*system_args, fail=False)
        if not is_continue: return

def limit_cycle_find_check(params):
    IC, T, *system_args = params
    system_args = tuple(system_args)
    assert IC[0] == 0 # Main Convention

    try:
        T, IC = limit_cycles.find_limit_cycle(R_SIDES.coupled_pendulums_rs, system_args, IC, T,
            phase_period=2*mt.pi,
            eps=1e-5)
        return True
    except ArithmeticError:
        return False

def calcline_limit_cycle(params, param_politics, filename_for_dump):
    IC, T, *system_args = params
    system_args = tuple(system_args)

    while True:
        while True:
            try:
                T, IC = limit_cycles.find_limit_cycle(R_SIDES.coupled_pendulums_rs, system_args, IC, T,
                    phase_period=2 * mt.pi,
                    method='broyden1',
                    eps=1e-7)
                break
            except ArithmeticError:
                is_continue, system_args = param_politics.update(*system_args, fail=True)
                if not is_continue: return

        d = {"system args": system_args, "Limit Cycle Period": T, "Initial Conditions": IC}
        dump(d, filename_for_dump)

        is_continue, system_args = param_politics.update(*system_args, fail=False)
        if not is_continue: return

def calcline_stability(filename_for_get_data, filename_for_dump):
    with open(filename_for_get_data, 'rb') as f:
        while True:
            try:
                d = pickle.load(f)
                system_args = d.get("system args")
                T = d.get("Limit Cycle Period")
                IC = d.get("Initial Conditions")

                M_eta = limit_cycles.get_monogrommy_matrix(R_SIDES.coupled_pendulums_rs,
                                            R_SIDES.coupled_pendulums_rs_linear_eta,
                                            IC, T,
                                            system_args, system_args)

                M_ksi = limit_cycles.get_monogrommy_matrix(R_SIDES.coupled_pendulums_rs,
                                            R_SIDES.coupled_pendulums_rs_linear_ksi,
                                            IC, T,
                                            system_args, system_args)

                eta_eig, _  = get_eigenvalues(M_eta)
                ksi_eig, _ = get_eigenvalues(M_ksi)

                d = {"system args": system_args,"Limit Cycle Period": T, "Initial Conditions": IC,
                    "eta_eig": eta_eig, "ksi_eig": ksi_eig}

                dump(d, filename_for_dump)

            except EOFError:
                break
