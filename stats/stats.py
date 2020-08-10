"""
File: stats.py
Author: Jeremy Ephron
---------------------
This file implements various statistical functions.

"""

from typing import Union

import numpy as np
import pandas as pd

from utils import make_comparable


def normalize(
    a: Union[pd.DataFrame, pd.Series]
) -> Union[pd.DataFrame, pd.Series]:
    """
    Normalizes a data stream.

    Args:
        a: The DataFrame or Series to normalize.

    Returns:
        The DataFrame or Series min-max normalized.

    """

    return (a - a.min()) / (a.max() - a.min())


def standardize(
    a: Union[pd.DataFrame, pd.Series]
) -> Union[pd.DataFrame, pd.Series]:
    """
    Standardizes a data stream.

    Args:
        a: The DataFrame or Series to standardize.

    Returns:
        The DataFrame or Series with mean of 0 and standard deviation of 1.

    """

    return (a - a.mean()) / a.std()


def relativize_to_avg(a: pd.DataFrame) -> pd.DataFrame:
    """
    Subtracts the daily global average from each day's values.

    Args:
        a: The DataFrame to relativize.

    Returns:
        The DataFrame with each row's average subtracted out.

    """

    return a.sub(a.mean(axis=1), axis=0)


def sigmoid(
    x: Union[float, pd.Series],
    lb: float = -1, 
    ub: float = 1, 
    scale: float = 1,
    deg: int = 1,
) -> Union[float, pd.Series]:
    """
    Applies a sigmoid function to x that is asymptotically bounded between ub
    and lb.
    
    Args:
        x: The value or series of values to apply the sigmoid to.
        lb: The lower bound.
        ub: The upper bound.

    Returns:
        The sigmoid function evaluated on x (or each value within x), bounded 
        between ub and lb.

    """
    
    sig = (1 / (1 + np.exp(-scale * x**deg))) * (ub - lb) + lb
    if deg % 2 == 0:
        return np.sign(x) * sig
    else:
        return sig


def compute_corrcoef(
    a: Union[pd.DataFrame, pd.Series],
    b: Union[pd.DataFrame, pd.Series]
) -> Union[float, np.array]:
    """
    Computes the correlation coefficients country-wise between two DataFrames.
    
    If a and b are series simply returns the correlation coefficient between 
    the two.

    Args:
        a: The first DataFrame or series.
        b: The second DataFrame or series.

    Returns:
        coef: An array containing the correlation coefficients between each 
            country's corresponding series in a and b, or the coefficent 
            between the two series if a and b are Series objects.

    """

    assert type(a) == type(b)
    
    if isinstance(a, pd.Series):
        return np.corrcoef(*make_comparable(a, b))[0,1]

    b = b[a.columns]
    assert (a.columns == b.columns).all()

    coef = np.zeros(a.shape[1])
    for i, country in enumerate(a.columns):
        coef[i] = np.corrcoef(*make_comparable(a[country], b[country]))[0,1]

    return coef

