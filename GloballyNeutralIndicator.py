#develop a globally neutral indicator, that takes in 2 countries, and returns signals
def cross_country(countryA, countryB):
    m2 = dl.pull("M2/inUSD")[countryA]
    m2 = m2.to_frame("supply_A")    
    m2["supply_B"] = dl.pull("M2/inUSD")[countryB]

    m2["year-month"] = m2.index.to_series().astype(str)
    m2["rolling_m3_A"] = m2["supply_A"].rolling(3).mean()
    m2["rolling_m12_A"] = m2["supply_A"].rolling(12).mean()
    m2["m12-m3_A"] = m2["rolling_m12_A"] - m2["rolling_m3_A"]
    
    m2["rolling_m3_B"] = m2["supply_B"].rolling(3).mean()
    m2["rolling_m12_B"] = m2["supply_B"].rolling(12).mean()
    m2["m12-m3_B"] = m2["rolling_m12_B"] - m2["rolling_m3_B"]
    
    m2["standardized"] = 0
    m2["signal_strength"] = 0
    m2["normalized"] = 0


    count = 0
    for i in ["A", "B"]:
        for (index_label, row_series) in m2.iterrows():
            label = str(index_label)
            m2.at[label, "standardized_sd"] = m2["m12-m3_"+i][:count].std()
            m2.at[label, "standardized_mean"] = m2["m12-m3_"+i][:count].mean()
            z_score = (m2.at[label, "m12-m3_"+i]-m2.at[label, "standardized_mean"])/m2.at[label, "standardized_sd"]

            m2.at[label, "signal_strength_"+i] = z_score
            m2.at[label, "normalized"+i] = (norm.cdf(z_score)-.5)*2
            count += 1
    
    #make sure to account for lag
    m2["difference_in_Z"] = m2["signal_strength_A"] - m2["signal_strength_B"]
      
    for (index_label, row_series) in m2.iterrows():
        label = str(index_label)
        m2.at[label, "standardized_sd"] = m2["difference_in_Z"][:count].std()
        m2.at[label, "standardized_mean"] = m2["difference_in_Z"][:count].mean()
        z_score = (m2.at[label, "difference_in_Z"]-m2.at[label, "standardized_mean"])/m2.at[label, "standardized_sd"]

        m2.at[label, "signal_strength_diff"] = z_score
        m2.at[label, "normalized_diff"] = (norm.cdf(z_score)-.5)*2
        count += 1
    return m2  