Bridgewater Internship 2020 (UNDER CONSTRUCTION)
================================================

The two most relevant files to look at are [indicators.py](indicators.py) and [stats.py](stats/stats.py).


Notice about Sharpe Ratios
--------------------------

After further investigation and extensive discussion, it appears that all the math for computing Sharpe ratios is correct, but that the resulting Sharpe ratio, computed by annualizing a daily Sharpe ratio may give less useful numbers than a ratio computed on a year-over-year or even a month-over-month basis. Potentially due to autocorrelation between daily bond returns, and the fact that this was computed over a period of fantastic returns, this leads to a higher Sharpe ratio, that may be less helpful in making a decision about the future (which is what investment decisions ultimately need to do).

Because of this, I advise that all numbers and results be viewed for precisely what they are (still mathematically correct) and not given any more weight than that in terms of understanding this strategy's success over longer periods and moving forward.

I will need to spend some time carefully reworking pieces of this in light of this new understanding, and will update this notice and the repository at that time.
