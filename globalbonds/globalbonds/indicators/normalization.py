

def center_using_historical_rolling_mean(tbl, window=6, gap=1):
    """Return a centered DataFrame.

    Center using a rolling mean calculated only on historical data.

    Default is to use previous five months to center current month
    e.g. center June using Jan-May
    """
    center = tbl.mean(axis=1).rolling(window).apply(
        lambda x: x[:window - gap].mean()
    )
    centered = (tbl.T - center).T
    return centered


def scale_using_historical_rolling_max(centered, window=6, gap=1):
    """Return a scaled DataFrame.

    Scale using a rolling mean of max values calculated only on
    historical data.

    Default is to use previous five months to scale current month
    e.g. scale June using Jan-May
    """
    centered_scaled = (centered.T / centered.abs().max(axis=1)).T
    scale = centered.abs().max(axis=1).rolling(window).apply(
        lambda x: x[:window - gap].mean()
    )
    centered_scaled = (centered.T / scale).T
    return centered_scaled


def center_scale_using_historical_rolling(tbl, window=6, gap=1):
    """Return a centered and scaled DataFrame."""
    centered = center_using_historical_rolling_mean(tbl, window=window, gap=gap)
    centered_scaled = scale_using_historical_rolling_max(centered, window=window, gap=gap)
    centered_scaled_timed = centered_scaled.resample('M').mean()
    return centered_scaled_timed
