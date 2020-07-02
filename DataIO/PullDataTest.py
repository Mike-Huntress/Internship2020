from pydatastream import Datastream
from DataIO.DataLib import datastream, DataLib, DatastreamPulls


DS = Datastream(username="ZBDW073", password="MOTOR315")

#data = DS.get_price('@AAPL', date_from='2008', date_to='2009')
# data = DS.fetch(['USCGDP..D'], date_from='2000')
#
# print(data)


dl = DataLib("Short Rate")
data = DS.fetch(['USCGDP..D'], date_from='2000')
dl.write_csv("Short Rate", data)

print(dl.lst())

# dsPuller = DatastreamPulls.ds_country_pull()
# dsPuller





