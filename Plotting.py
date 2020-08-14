def pnl_series(signals, bankroll, country, start=0, end=0):
    
    #if signals data is monthly and not daily
    BondReturnIndex = dl.pull('BondRetIdx/LocalFX')[country]
    BondReturnIndex = BondReturnIndex.to_frame("return")

    BondReturnIndex["daily_change"] = np.exp(np.log(BondReturnIndex["return"]).diff(1))
    BondReturnIndex["full-date"] = BondReturnIndex.index.to_series().astype(str)
    BondReturnIndex["year-month"] = BondReturnIndex['full-date'].str.slice(0, 7)

    merged = BondReturnIndex.set_index("year-month").join(signals[['year-month', "signal_strength"]].set_index("year-month"), on="year-month", how='left', lsuffix="-og")
    #merged["signal"] = merged["signal"].shift(44)
    merged["signal_strength"] = merged["signal_strength"].shift(44)
    

    merged['net_for_day'] = merged['signal_strength'] * (merged['daily_change']-1) * bankroll #calculation
    merged = merged.set_index("full-date")
    
    cumulative = merged["net_for_day"].cumsum()

    return cumulative, merged


def plot_pnl(pnl_values, indicator, table, country):
    table = table["return"]
    first_val = table.first_valid_index()
    table = table.fillna(0)
    table = table - table[first_val]
    #table = table.set_index("full-date")
    
    pnl_values = pnl_values.to_frame().set_index(pd.to_datetime(pnl_values.index))
    
    fig, ax1 = plt.subplots()
    ax1_label = 'Profit and Loss'
    ax1.plot(pnl_values, label = indicator)
    ax1.set_ylabel(ax1_label)
    #ax1.plot(table, color = 'tab:red', label = "Bond Return Index")
    ax1.legend()
    plt.title("{0} vs Bond Return Index".format(indicator+" " + country))
    plt.show() 