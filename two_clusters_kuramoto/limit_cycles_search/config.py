import numpy as np
import math as mt

class Config:
    data_storage = './data'
    N = 5
    K = 2
    Alpha = mt.pi / 2
    Mass_end = 5
    T0 = 80
    IC0 = np.array([0, 0.15])
