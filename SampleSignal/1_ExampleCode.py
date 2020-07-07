from BasicSetupUtilities.MetaDataBuilder import CountryMetaDataFile
from DataIOUtilities.DataLib import DataLib

countries = CountryMetaDataFile().readMetadata()
dl = DataLib("SignalData")


LongRates = dl.pull("LongRates")
#Simple period-over-period Diff
LongRates_Change = LongRates.diff()

#Difference between series
ShortRates = dl.pull("ShortRates")
LRMinusSR = LongRates - ShortRates
print(LRMinusSR.head)









