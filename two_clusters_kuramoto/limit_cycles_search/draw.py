import numpy as np
from config import Config
import seaborn as sns
import math as mt
import matplotlib.pyplot as plt
import pickle


from scipy.integrate import odeint
from rside import R_SIDES

iteration = 0

def main():
    with open(f'{Config.data_storage}/{iteration}.pickle', 'rb') as f:
        ARGS = pickle.load(f)
        T = pickle.load(f); IC = pickle.load(f)

        h = 1e-3; t = np.arange(0, 2 * T, h)
        data = odeint(R_SIDES.coupled_pendulums_rs, IC, t, ARGS)
        sns.lineplot(x=t, y=data[:, 1],label='frequency')
        plt.savefig('example.png')
        print("OK")

if __name__ == '__main__':
    main()
