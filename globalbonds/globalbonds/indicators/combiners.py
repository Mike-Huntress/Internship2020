

class Combiner:
    """Namespace class for combiner functions. No actual state."""

    def mean_value(tbl):
        """Return the mean value of the last row of tbl."""
        return tbl.iloc[-1].mean()

    def median_value(tbl):
        """Return the median value of the last row of tbl."""
        return tbl.iloc[-1].median()

    def mean_first_derivative(tbl):
        """Return the first derivative of the mean value."""
        means = tbl.mean()
        if means.shape[0] < 2:
            return float('nan')
        first_deriv = means.iloc[-1] - means.iloc[-2]
        return first_deriv

    def median_first_derivative(tbl):
        """Return the first derivative of the mean value."""
        medians = tbl.median()
        if medians.shape[0] < 2:
            return float('nan')
        first_deriv = medians.iloc[-1] - medians.iloc[-2]
        return first_deriv
