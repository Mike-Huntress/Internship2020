
from plotnine import *


class TimeSeriesSet:
    """Wrapper for a pandas dataframe that holds several time series."""

    def __init__(self, tbl):
        self.tbl = tbl

    def get_internal_correlation(kind='normal'):
        """Return a DataFrame with internal correlation."""
        pass

    def get_internal_proportionality(kind='normal'):
        """Return a DataFrame with internal proportionality."""
        pass

    def long_form(self, name='date'):
        tbl = self.tbl
        tbl[name] = tbl.index.to_series().map(lambda x: x.to_timestamp())
        tbl = tbl.melt(id_vars=name)
        return tbl

    def plot(self, ylabel='value', inject=lambda x: x):
        tbl = self.long_form()
        tbl = inject(tbl)
        return (
            ggplot(tbl, aes(x='date', y='value', color='country')) +
                geom_line() +
                geom_point() +
                scale_color_brewer(type='qualitative', palette=3) +
                ylab(ylabel) +
                xlab('Date') +
                scale_x_date() +
                theme(
                    text=element_text(size=20),
                    figure_size=(12, 8),
                    legend_position='right',
                    axis_text_x=element_text(size=20, angle=90, hjust=0),
                    panel_border=element_rect(colour="black", size=2),
                )
        )
