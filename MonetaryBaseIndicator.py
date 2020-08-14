#takes in a country name, and returns signals for that country, on a daily basis
def monetary_base_signals(country):
    m2 = dl.pull("M2/inUSD")[country]
    m2 = m2.to_frame("supply")

    m2["year-month"] = m2.index.to_series().astype(str)
    m2["diff_3"] = np.exp(np.log(m2["supply"]).diff(3))
    m2["diff_12"] = np.exp(np.log(m2["supply"]).diff(12))

    m2["m12-m3"] = m2["diff_12"] - m2["diff_3"]
    m2["standardized"] = 0
    m2["signal_strength"] = 0
    m2["normalized"] = 0


    count = 0
    for (index_label, row_series) in m2.iterrows():
        label = str(index_label)
        m2.at[label, "standardized_sd"] = m2["m12-m3"][:count].std()
        m2.at[label, "standardized_mean"] = m2["m12-m3"][:count].mean()
        z_score = (m2.at[label, "m12-m3"]-m2.at[label, "standardized_mean"])/m2.at[label, "standardized_sd"]

        m2.at[label, "signal_strength"] = z_score
        m2.at[label, "normalized"] = (norm.cdf(z_score)-.5)*2
        count += 1

    return m2