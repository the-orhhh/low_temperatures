import numpy as np
from scipy.optimize import curve_fit

def type_i_curve(t, T=1.0, A=1.0, B=0.0):
    t = np.asarray(t)
    y = np.full_like(t, B, dtype=float)
    mask = (t >= 0) & (t < T)
    y[mask] = A * (2*(t[mask]/T) - 1) + B
    return y

def fit_type_i(time, data):
    popt, pcov = curve_fit(type_i_curve, time, data, p0=[1.0, 1.0, 0.0])
    return popt, pcov

def type_ii_curve(t, T=1.0, A=1.0, B=0.0):
    t = np.asarray(t)
    y = np.full_like(t, B, dtype=float)
    mask1 = (t >= 0) & (t < T/2)
    mask2 = (t >= T/2) & (t < T)
    y[mask1] = A * (4*(t[mask1]/T)) + B
    y[mask2] = A * ( -4*(t[mask2]/T) + 4 ) + B
    return y

def fit_type_ii(time, data):
    popt, pcov = curve_fit(type_ii_curve, time, data, p0=[1.0, 1.0, 0.0])
    return popt, pcov