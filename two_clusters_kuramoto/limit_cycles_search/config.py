import numpy as np
import math as mt

class Config:
    data_storage = './data'
    N, K, Alpha = 5, 2, mt.pi / 2
    T0 = 80
    IC0 = np.array([0, 0.15])
    Mass_end = 10
