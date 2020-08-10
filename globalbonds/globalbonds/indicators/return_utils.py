
import pandas as pd
import numpy as np


def signalize(scores):
    """Return a DataFrame where all rows sum to zero and the largest absolute value is 1."""
    scores = scores.T
    scores = scores - scores.mean()
    scores = scores / scores.abs().max()
    scores = scores.T
    return scores


def get_momentum_signal(bond_returns, window=4):
    """Return a DataFrame with a momentum signal.

    momentum signal - i.e. do what worked before
    """
    momentum_signal = bond_returns.pct_change() + 1
    momentum_signal = momentum_signal.rolling(window).apply(lambda x: x[:window - 1].mean())
    momentum_signal = signalize(momentum_signal)
    return momentum_signal


def get_optimal_signal(bond_returns):
    """Return a DataFrame with an 'optimal' signal for a set of bonds.

    Optimal in this case means a set of market-neutral trades that would
    produce the largest possible returns (identified with the benefit of hindsight).
    This means going 100% long on the highest returner and 100% short on the
    lowest returner (even if the lowest returner is positive).
    """
    optimal_signal = (bond_returns.pct_change() + 1)

    def minmaxsig(row):
        out = row.copy().fillna(0)
        out[:] = 0
        out[row.idxmax()] = 1
        out[row.idxmin()] = -1
        return out

    optimal_signal = optimal_signal.apply(minmaxsig, axis=1)
    optimal_signal = optimal_signal.drop(columns=optimal_signal.columns[-1])
    return optimal_signal


def get_random_signal(bond_returns):
    """Return a DataFrame with a uniform random signal for a set of bonds."""
    random_signal = np.random.random(size=bond_returns.shape)
    random_signal = pd.DataFrame(
        random_signal, columns=bond_returns.columns, index=bond_returns.index
    )
    random_signal = signalize(random_signal)
    return random_signal


def get_risk_free_return(bond_returns):
    risk_free_returns = bond_returns['USA'].pct_change() + 1
    risk_free_returns = risk_free_returns.cumprod()
    return risk_free_returns


def calc_signal_returns(bond_returns, signal):
    """Return a Series of returns (as fraction of initial investment) for a signal."""
    signal = signal.copy().fillna(0)
    bond_returns = bond_returns.pct_change()
    bond_returns = bond_returns.fillna(0)
    bond_returns += 1

    signal_returns = bond_returns * signal
    signal_returns = (signal_returns.sum(axis=1) + 1)
    signal_returns = signal_returns.cumprod()
    return signal_returns
