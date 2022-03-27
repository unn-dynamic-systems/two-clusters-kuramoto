
import matplotlib.pyplot as plt
import os
import sys
from numpy.linalg import norm
import pickle
from existance_zones.existance_zones import M as M_function

def read_pickle(file):
    res = []
    while True:
        try:
            res.append(pickle.load(file))
        except EOFError:
            break
    return res


def is_stable(*p):
    for p_i in p:
        if norm(p_i) > 1:
            return False
    return True

def main():
    FOLDER_TO_GET = sys.argv[1]
    if not os.path.exists(f"{FOLDER_TO_GET}"):
        print(f"Not found {FOLDER_TO_GET}")
        exit(1)

    files = os.listdir(f"{FOLDER_TO_GET}")

    for f in files:
        with open(f"{FOLDER_TO_GET}/{f}", 'rb') as file:
            data_file = read_pickle(file)
            for d in data_file:
                N, Mass, Alpha, K = d.get("system args")
                IC = d.get("Initial Conditions")
                T = d.get("Limit Cycle Period")
                plt.title(f'N={N}, K={K}')
                eta_eig = d.get("eta_eig")
                ksi_eig = d.get("ksi_eig")
                print(Alpha, Mass)
                print(IC, T)
                print(eta_eig)
                # print(ksi_eig)
                # print(is_stable(eta_eig, ksi_eig))
                plt.plot(Alpha, Mass, marker='o', markersize=3, color="b" if is_stable(eta_eig) else "r")
    
    plt.xlabel('alpha')
    plt.ylabel('mass')
    plt.plot()
    plt.savefig("eexx.png")
if __name__ == "__main__":
    main()
