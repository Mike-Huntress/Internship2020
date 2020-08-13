#Utility functions
import matplotlib.pyplot as plt


def align_yaxis(ax1, v1, ax2, v2):
    _, y1 = ax1.transData.transform((0, v1))
    _, y2 = ax2.transData.transform((0, v2))
    inv = ax2.transData.inverted()
    _, dy = inv.transform((0, 0)) - inv.transform((0, y1-y2))
    miny, maxy = ax2.get_ylim()
    ax2.set_ylim(miny+dy, maxy+dy)


'''plot_vs_returns plots a signal against returns
countries - list of countries to plot
series - signal df
returns - bond metric df
tfs - list of time chunks (refer to notebook file)
scale - flag for formatting options
correlation - whether or not to display correlation value
'''


def plot_vs_returns(countries, series, returns, tfs, scale=True, correlation=False):
    for tf in tfs:
        print(tf)
        for country in countries:
            fig, ax1 = plt.subplots()
            ax2 = ax1.twinx()
            ax1.plot(series.loc[tf[0]:tf[1], country].to_timestamp(), color="purple", alpha=.7)
            ax2.plot(returns.loc[tf[0]:tf[1], country].to_timestamp(), color="green", alpha=.3)
            if scale:
                ax1.set(ylim=(-.2, .2))
                ax2.set(ylim=(-.2, .2))
            ax1.legend(["Indicator"], loc='upper right')
            ax2.legend(["Relative Bond Performance"], loc="lower left")
            plt.title(country)
            plt.show()
            if correlation:
                print(returns.loc[tf[0]:tf[1], country].resample('M').last().corr(series.loc[tf[0]:tf[1], country]))


'''create_p_and_l returns a dataframe with P&L for each country
signal - trading signal
bond_idx - the bond index
countries_order - a list of countries to specify column ordering
'''


def create_p_and_l(signal, bond_idx, countries_order):
    signal_quarterly = signal.resample("Q").last()
    bond_idx_quarterly = bond_idx.resample("Q").last()
    bond_idx_quarterly_shifted = bond_idx_quarterly.shift(-1)
    quarterly_returns_shifted = bond_idx_quarterly_shifted.pct_change(1)
    p_and_l = signal_quarterly[countries_order] * quarterly_returns_shifted[countries_order]
    return p_and_l
