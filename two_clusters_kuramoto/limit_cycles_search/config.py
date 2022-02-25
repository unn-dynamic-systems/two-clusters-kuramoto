import numpy as np
import math as mt

class Config:
    data_storage = './data'
    H_M = 1e-1
    N, K, Alpha = 5, 2, mt.pi / 2
    T0 = 80
    IC0 = np.array([0, 0.15])
    Mass_end = 80
