import numpy as np

class Config:
    data_storage = './data'
    H_M = 1e-1
    N, Mass, Alpha, Omega = 6, 3, 1.2, 1.3
    T0 = 4.01739166e+00
    IC0 = np.array([0, 4.00489756e+00, 6.83138901e-01, 2.81285526e+00,
                   6.83138901e-01, 2.81285526e+00, 0, 4.00489756e+00,
                   0, 4.00489756e+00, 6.83138901e-01, 2.81285526e+00])
