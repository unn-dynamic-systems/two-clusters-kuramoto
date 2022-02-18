import numpy as np
from config import Config
import seaborn as sns
import matplotlib.pyplot as plt
import pickle


from scipy.integrate import odeint
from rside import R_SIDES

iteration = 0

def main():
    with open(f'{Config.data_storage}/{iteration}.pickle', 'rb') as f:
        ARGS = pickle.load(f)
        T = pickle.load(f); IC = pickle.load(f)
        M = pickle.load(f); E = pickle.load(f)

        print(IC)
        print(T)
        print(ARGS)

        h = 1e-3; t = np.arange(0, T, h)
        N = ARGS[0]
        # data = odeint(R_SIDES.coupled_pendulums_rs, IC, t, ARGS)

        np.random.seed(42); q0 = np.random.rand(2 * N)
        data = odeint(R_SIDES.coupled_pendulums_rs, q0, t, ARGS)
        for i in range(N):
            sns.lineplot(x=t, y=data[:, 1 + 2 * i])
        plt.savefig('example.png')
        print("OK")

if __name__ == '__main__':
    main()