"""
File: utils.py
Author: Jeremy Ephron
---------------------
This file implements various utility functions to be used throughout the 
project.

These functions are mainly for convenience or are otherwise more administrative
in nature.

"""

from typing import Tuple

import pandas as pd


# 253 trading days in the US market:
#     365.25 (days on average per year)
#   * 5/7 (proportion work days per week)
#   - 6 (weekday holidays)
#   - 3 * 5/7 (fixed date holidays)
#   -------------------------------------
#     252.75 ~> 253
#
# But empirically each year has ~261 datapoints (why is that?)
WEEKDAYS_PER_YEAR = 261
DAYS_PER_YEAR = 365
MONTHS_PER_YEAR = 12
QUARTERS_PER_YEAR = 4
WEEKDAYS_PER_QUARTER = int(WEEKDAYS_PER_YEAR / QUARTERS_PER_YEAR)
WEEKDAYS_PER_MONTH = int(WEEKDAYS_PER_YEAR / MONTHS_PER_YEAR)
MONTHS_PER_QUARTER = int(MONTHS_PER_YEAR / QUARTERS_PER_YEAR)


def make_comparable(a: pd.Series, b: pd.Series) -> Tuple[pd.Series, pd.Series]:
    """
    Makes two series comparable by aligning, dropping missing values, and 
    resampling to the larger frequency by averaging.

    Args:
        a: The first series.
        b: The second series.

    Returns:
        The two modified series.

    """

    common_dt = pd.to_datetime('2000-01-01')
    if common_dt + a.index.freq > common_dt + b.index.freq:
        b = b.resample(a.index.freq).mean()
    elif common_dt + a.index.freq < common_dt + b.index.freq:
        a = a.resample(b.index.freq).mean()
    
    a = a.reindex(b.dropna().index).dropna()
    b = b.reindex(a.index)
    return a, b

