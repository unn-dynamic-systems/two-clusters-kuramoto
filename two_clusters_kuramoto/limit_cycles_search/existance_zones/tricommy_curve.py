import numpy as np
import math as mt
import pickle
from numba import njit

# Remove it if you are installed our module already
import os; cwd = os.path.dirname(os.path.abspath(__file__))
package_path = os.path.normpath(os.path.join(cwd, "..", "..", "..", "calculation"))
import sys; sys.path.append(package_path)

# Every import of our library should looks like this
from unn_ds import optimizers

def main():

    @njit
    def tricommy_curve(x):
        return 4 / mt.pi * x - 0.305 * x ** 3
    
    def tricommy_curve_inv(x):
        @njit
        def wrap(y):
            tc = tricommy_curve(y)
            return (x - tc) ** 2
        
        return optimizers.newton(wrap, np.array([0.5]), eps=1e-6)
    
    h = 1e-2
    a, b = 0, 1
    intervals = int((b - a) / h)
    x = np.linspace(a, b, intervals)
    y = np.array([tricommy_curve_inv(x_i)[0] for x_i in x])
    with open(f'tricommy_curve_inv_{a}_to_{b}_h_{h}.pickle', 'wb') as f:
        pickle.dump(x, f)
        pickle.dump(y, f)

if __name__ == '__main__':
    main()
