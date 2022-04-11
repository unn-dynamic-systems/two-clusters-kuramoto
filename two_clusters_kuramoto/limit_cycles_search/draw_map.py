
import matplotlib.pyplot as plt
import os
import sys
import numpy as np
from numpy.linalg import norm
import pickle
from tqdm import tqdm

def read_pickle(file):
    res = []
    while True:
        try:
            res.append(pickle.load(file))
        except EOFError:
            break
    return res


def is_stable(*p):
    return (np.absolute(p) < 1).all()

def main():
    FOLDER_TO_GET = sys.argv[1]
    if not os.path.exists(f"{FOLDER_TO_GET}"):
        print(f"Not found {FOLDER_TO_GET}")
        exit(1)

    files = os.listdir(f"{FOLDER_TO_GET}")
    bpar = tqdm(total=len(files))
    for f in files:
        bpar.update(1)
        with open(f"{FOLDER_TO_GET}/{f}", 'rb') as file:
            data_file = read_pickle(file)
            for d in data_file:
                N, Mass, Alpha, K = d.get("system args")
                IC = d.get("Initial Conditions")
                T = d.get("Limit Cycle Period")
                plt.title(f'N={N}, K={K}')
                eta_eig = d.get("eta_eig")
                ksi_eig = d.get("ksi_eig")
                plt.plot(Alpha, Mass, marker='o', markersize=1, color="b" if is_stable(ksi_eig, eta_eig) else "r")
    
    plt.xlabel('alpha')
    plt.ylabel('mass')
    plt.show()
    # plt.savefig("eexx.png")
if __name__ == "__main__":
    main()
