#function that takes in the signals (list), name of an indicator (string), and a country name (string)
def pnl_single_country(signals, indicator, country):
    pnl_values, table = pnl_series(signals, 100, country)
    
    table = table["return"]
    first_val = table.first_valid_index()
    table = table.fillna(0)
    table = table - table[first_val]
    #table = table.set_index("full-date")
    
    pnl_values = pnl_values.to_frame().set_index(pd.to_datetime(pnl_values.index))
    return pnl_values

def pnl_helper(signals, bankroll, country, start=0, end=0):
    
    #if signals data is monthly and not daily
    BondReturnIndex = dl.pull('BondRetIdx/LocalFX')[country]
    BondReturnIndex = BondReturnIndex.to_frame("return")

    BondReturnIndex["daily_change"] = np.exp(np.log(BondReturnIndex["return"]).diff(1))
    BondReturnIndex["full-date"] = BondReturnIndex.index.to_series().astype(str)
    BondReturnIndex["year-month"] = BondReturnIndex['full-date'].str.slice(0, 7)

    merged = BondReturnIndex.set_index("year-month").join(signals[['year-month', "normalized", "supply"]].set_index("year-month"), on="year-month", how='left', lsuffix="-og")
    #merged["signal"] = merged["signal"].shift(44)
    merged["normalized"] = merged["normalized"].shift(22)
    

    merged['net_for_day'] = merged['normalized'] * (merged['daily_change']-1) * bankroll #calculation
    merged = merged.set_index("full-date")
    
    cumulative = merged["net_for_day"].cumsum()

    return cumulative, merged

#function that takes in 2 country names and dataset (signals derived from the GloballyNeutralIndicator.py)
def pnl_multiple_country(dataset, country1, country2):
    BondReturnIndex = dl.pull('BondRetIdx/LocalFX').resample("M").mean()
    BondReturnIndex["change_1"] = np.exp(np.log(BondReturnIndex[country1]).diff(1))
    BondReturnIndex["change_2"] = np.exp(np.log(BondReturnIndex[country2]).diff(1))
    
    BondReturnIndex["pnl_1"] = dataset["normalized_diff"] * (BondReturnIndex["change_1"] -1) * 100
    BondReturnIndex["pnl_2"] = dataset["weight_usa"] * (BondReturnIndex["change_2"] -1)*100
    
    BondReturnIndex["net"] = -1*(BondReturnIndex["pnl_1"] + BondReturnIndex["pnl_2"])
    
    return BondReturnIndex["net"].cumsum()