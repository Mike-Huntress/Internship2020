import os, shutil, configparser
import pandas as pd

class CountryMetaData:
    def __init__(self, id, DataStreamCode, Name, DataStreamCurr):
        self.id = id
        self.DataStreamCode = DataStreamCode
        self.Name = Name
        self.DataStreamCurr = DataStreamCurr
    def id(self):
        self.id
    def DataStreamCode(self):
        self.DataStreamCode
    def Name(self):
        self.Name
    def DataStreamCurr(self):
        self.DataStreamCurr
    def print(self):
        print("id:"+self.id+"; DataStreamCode:"+self.DataStreamCode+"; Name:"+self.Name+"; DataStreamCurr:"+self.DataStreamCurr)

def buildCountryMetaDataRow(id, DataStreamCode, Name, DataStreamCurr):
    config = configparser.ConfigParser()

    config.add_section(id)
    config[id]['id'] = id
    config[id]['DataStreamCode'] = DataStreamCode
    config[id]['Name'] = Name
    config[id]['DataStreamCurr'] = DataStreamCurr

    with open("countryMetaData.ini", 'w') as f:
        config.write(f)

class CountryMetaDataFile:
    user_config_dir = os.path.expanduser("~") + "/.datalib"
    user_config = user_config_dir + "/countryMetaData.ini"

    def _init__(self):
        self

    def addCountry(self, id, DataStreamCode, Name, DataStreamCurr):
        if not os.path.isfile(self.user_config):
            os.makedirs(self.user_config_dir, exist_ok=True)
            buildCountryMetaDataRow(id, DataStreamCode, Name, DataStreamCurr)
            shutil.copyfile("countryMetaData.ini", self.user_config)
            os.remove("countryMetaData.ini")

        config = configparser.ConfigParser()
        config.read(self.user_config)

        if not config.has_section(id):
            config.add_section(id)

        config[id]['id'] = id
        config[id]['DataStreamCode'] = DataStreamCode
        config[id]['Name'] = Name
        config[id]['DataStreamCurr'] = DataStreamCurr

        ##Write
        with open(self.user_config, 'w') as f:
            config.write(f)


    def readCountryMeta(self):
        config = configparser.ConfigParser()
        config.read(self.user_config)
        d = []
        for country in config.sections():
            d.append(
                {
                    'id': config[country]['id'],
                    'DataStreamCode': config[country]['DataStreamCode'],
                    'Name': config[country]['Name'],
                    'DataStreamCurr': config[country]['DataStreamCurr']
                }
            )
        return pd.DataFrame(d)



CountryMetaDataFile().addCountry("USA", "US", "United States", "USD")
CountryMetaDataFile().addCountry("JPN", "JP", "Japan", "JAP")
CountryMetaDataFile().addCountry("GBR", "UK", "Great Britain", "UKP")
CountryMetaDataFile().addCountry("CAN", "CN", "Canada", "CAD")
CountryMetaDataFile().addCountry("AUS", "AU", "Australia", "AUD")
CountryMetaDataFile().addCountry("SWE", "SD", "Sweden", "SWF")
CountryMetaDataFile().addCountry("NOR", "NW", "Norway", "NOR")
CountryMetaDataFile().addCountry("ESP", "ES", "Spain", "ESP")
CountryMetaDataFile().addCountry("ITA", "IT", "Italy", "ITL")
CountryMetaDataFile().addCountry("DEU", "BD", "Germany", "WGM")


print(CountryMetaDataFile().readCountryMeta())



