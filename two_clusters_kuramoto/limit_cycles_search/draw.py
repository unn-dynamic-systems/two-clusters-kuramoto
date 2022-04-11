import numpy as np
import seaborn as sns
import math as mt
import matplotlib.pyplot as plt
import pickle


from scipy.integrate import odeint
from rside import R_SIDES

iteration = 0

def main():
    ARGS = 9, 10, 1.57, 4
    T = 500
    IC = np.array([0, 0.2])

    h = 1e-3; t = np.arange(0, T, h)
    data = odeint(R_SIDES.coupled_pendulums_rs, IC, t, ARGS)
    sns.lineplot(x=t, y=data[:, 1],label=f'frequency')
    print("OK")
    plt.show()
if __name__ == '__main__':
    main()
