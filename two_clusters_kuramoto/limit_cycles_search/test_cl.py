import pickle
from rside import R_SIDES
from numpy.linalg import eig as get_eigenvalues
import numpy as np
# Remove it if you are installed our module already
import os; cwd = os.path.dirname(os.path.abspath(__file__))
package_path = os.path.normpath(os.path.join(cwd, "..", "..", "..", "calculation"))
import sys; sys.path.append(package_path)

# Every import of our library should looks like this
from unn_ds import limit_cycles

def dump(data, filename):
    with open(f'{filename}', 'ab') as f:
        pickle.dump(data, f)

def calcline_stability():
    args_orig = 5, 35.9, 1.0707963267948961, 1
    T = 11.963432017874139
    IC =  np.array([0, 0.55051525])

    M = limit_cycles.get_monogrommy_matrix(R_SIDES.coupled_pendulums_rs,
                                R_SIDES.coupled_pendulums_rs_linear_eta,
                                IC, T,
                                args_orig, args_orig)

    eta_eig, _  = get_eigenvalues(M)
    print(eta_eig)
    norm = np.linalg.norm(eta_eig)
    print(norm)
    is_stable = "UNSTABLE" if (norm > 1) else "STABLE"
    print(is_stable)


if __name__ == "__main__":
    calcline_stability()