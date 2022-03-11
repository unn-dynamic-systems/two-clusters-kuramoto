import pickle
import math as mt
from rside import R_SIDES

# Remove it if you are installed our module already
import os; cwd = os.path.dirname(os.path.abspath(__file__))
package_path = os.path.normpath(os.path.join(cwd, "..", "..", ".."))
import sys; sys.path.append(package_path)

# Every import of our library should looks like this
from calculation import limit_cycles


def dump(data, filename):
    with open(f'{filename}', 'ab') as f:
        pickle.dump(data, f)

def calcline(params, param_politics, filename_for_dump):
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
