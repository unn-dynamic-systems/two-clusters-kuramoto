import numpy as np
import math as mt

class Config:
    data_storage = './data'
    N = 5
    K = 1
    Alpha = mt.pi / 2
    Mass_start = 4.9
    Mass_end = 90
    T0 = 11.4
    IC0 = np.array([0, 0.5])
    h_m = 1
    h_m_limit = 1e-1
    h_a = 1e-1
    h_a_limit = 1e-3
