
import numpy as np
from scipy.stats import gmean, entropy
from numpy.linalg import norm


def extremity(row):
    return (row.max() - row.min()) / 2


def derivative(tbl, n=1, s=1):
    if n == 0:
        return tbl
    nrows = tbl.shape[0]
    prev = tbl.iloc[0:(nrows - s)]
    cur = tbl.iloc[s:nrows]
    prev.index = cur.index
    deriv = cur - prev 
    return derivative(deriv, n=n - 1)


def n_derivative_predict(tbl, n=1):
    first = derivative(tbl)
    if n == 1:
        forward_first = first
    else:
        forward_first = n_derivative_predict(first, n=n - 1)
    forward = tbl + forward_first
    forward = forward.iloc[:-1]
    forward.index = tbl.index[1:]
    return forward


def clr(X):
    _X = X + 0.0000001
    _X = _X / norm(_X, ord=1)
    g = gmean(_X)
    _X = np.divide(_X, g)
    _X = np.log(_X)
    return _X


def rho_proportionality(P, Q):
    _P, _Q = clr(P), clr(Q)
    N = np.var(_P - _Q)
    D = np.var(_P) + np.var(_Q)
    return 1 - (N / D)
