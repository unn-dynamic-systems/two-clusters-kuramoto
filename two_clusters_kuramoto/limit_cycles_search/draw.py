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
    with open(f'./data/limit_cycle/horizontal-line-4.99034-right.pickle', 'rb') as f:
        d = pickle.load(f)
        ARGS = d.get("system args")
        T = d.get("Limit Cycle Period")
        IC = d.get("Initial Conditions")

        h = 1e-3; t = np.arange(0, T, h)
        data = odeint(R_SIDES.coupled_pendulums_rs, IC, t, ARGS)
        sns.lineplot(x=t, y=data[:, 1],label='frequency')
        # sns.lineplot(x=t, y=data[:, 0],label='phase')
        plt.savefig('example.png')
        print("OK")

if __name__ == '__main__':
    main()
