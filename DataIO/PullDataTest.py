from pydatastream import Datastream
from DataIO.DataLib import datastream, DataLib, DatastreamPulls
from DataIO.MetaDataFile import CountryMetaDataFile


countries = CountryMetaDataFile().readMetadata()
# print(countries)


dsPuller = DatastreamPulls(countries)
start_date = '2000-01'
long_rates_primary = dsPuller.ds_country_pull(lambda x: f'TR{x}10T', start_date, 'RY', 'M', ["USA", "JPN"])

print(long_rates_primary)



##Write to DataLib
dl = DataLib("TestData")
#dl.write_data("Long_Rate", long_rates_primary.to_timestamp())

print(dl.pull("Long_Rate").loc[:,"USA"])


