"""
File: dfa.py
Author: Jeremy Ephron
---------------------

This file implements detrended fluctuation analysis (DFA).

TODO: describe DFA algorithm.

"""

from typing import Tuple

import numpy as np

def compute_dfa(
    x: np.array,
    window_min: float,
    window_max: float,
    window_step: float
) -> Tuple[np.array, np.array, float]:
    """
    Computes the detrended fluctuation analysis (DFA) exponent for the input 
    data and given window lengths.

    DFA is a method for determining the statistical self-affinity of a signal, 
    and the resulting DFA exponent can be interpreted as an estimate of the 
    Hurst exponent, but more robust to non-stationarities.

    To oversimplify, DFA can help identify self-similarity of a signal that 
    present in a statistical fashion that changes with time.

    Relevant Sources: 
        [1] https://journals.aps.org/pre/abstract/10.1103/PhysRevE.49.1685
        [2] https://www.frontiersin.org/articles/10.3389/fphys.2012.00450

    Args:
        x: the input data vector.
        window_min: the lower bound of the range of window lengths. These window
            lengths are given as exponents of powers of 2.
        window_max: the upper bound of the range of window lengths (exclusive).
        window_step: the step size between window lengths within the range.

    Returns:
        window_lens: the actual window lengths used.
        flucts: the fluctuation values observed.
        alpha: the DFA exponent.

    """

    # Compute the cumulative sum of the time series to create the signal profile
    y = np.cumsum(x - np.mean(x))

    window_lens = (
        2**np.arange(window_min, window_max, window_step)
    ).astype(np.int)
    flucts = np.zeros(len(window_lens))

    # Compute the detrended RMS for each window length
    for i, window_len in enumerate(window_lens):
        flucts[i] = np.sqrt(np.mean(
            compute_detrended_windowed_rms(y, window_len)**2
        ))

    # Linearly fit the resulting data
    coeff = np.polyfit(np.log2(window_lens), np.log2(flucts), 1)
    return window_lens, flucts, coeff[0]


def compute_detrended_windowed_rms(x: np.array, window_len: int) -> np.array:
    """
    Computes the root mean square (RMS) of the input data.

    Args:
        x: the input data vector,
        window_len: the length of the window over which to compute the RMS.

    Returns:
        rms: the RMS of each window. Output array will have dimension of 
            len(x) // window_len.

    """

    # Separate input data into windows
    windowed_shape = (x.shape[0] // window_len, window_len)
    x_windowed = np.lib.stride_tricks.as_strided(x, shape=windowed_shape)

    window_range = np.arange(window_len)
    rms = np.zeros(x_windowed.shape[0])

    # For each window, calculate the RMS of the detrended data
    for i, window in enumerate(x_windowed):

        # Compute the linear trend using least-squares fit
        coeff = np.polyfit(window_range, window, 1)
        trend = np.polyval(coeff, window_range)

        rms[i] = np.sqrt(np.mean((window - trend)**2))

    return rms
