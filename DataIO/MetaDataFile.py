import os, shutil, configparser
import pandas as pd

class CountryMetaData:
    def __init__(self, id, DatastreamCode, Name, DatastreamCurrency):
        self.id = id
        self.DatastreamCode = DatastreamCode
        self.Name = Name
        self.DatastreamCurrency = DatastreamCurrency
    def id(self):
        self.id
    def DatastreamCode(self):
        self.DatastreamCode
    def Name(self):
        self.Name
    def DatastreamCurrency(self):
        self.DatastreamCurrency
    def print(self):
        print("id:"+self.id+"; DatastreamCode:"+self.DataStreamCode+"; Name:"+self.Name+"; DatastreamCurrency:"+self.DatastreamCurrency)

def buildCountryMetaDataRow(id, DatastreamCode, Name, DatastreamCurrency):
    config = configparser.ConfigParser()

    config.add_section(id)
    config[id]['id'] = id
    config[id]['DatastreamCode'] = DatastreamCode
    config[id]['Name'] = Name
    config[id]['DatastreamCurrency'] = DatastreamCurrency

    with open("countryMetaData.ini", 'w') as f:
        config.write(f)

class CountryMetaDataFile:
    user_config_dir = os.path.expanduser("~") + "/.datalib"
    user_config = user_config_dir + "/countryMetaData.ini"

    def _init__(self):
        self

    def addCountry(self, id, DatastreamCode, Name, DatastreamCurrency):
        if not os.path.isfile(self.user_config):
            os.makedirs(self.user_config_dir, exist_ok=True)
            buildCountryMetaDataRow(id, DatastreamCode, Name, DatastreamCurrency)
            shutil.copyfile("countryMetaData.ini", self.user_config)
            os.remove("countryMetaData.ini")

        config = configparser.ConfigParser()
        config.read(self.user_config)

        if not config.has_section(id):
            config.add_section(id)

        config[id]['id'] = id
        config[id]['DatastreamCode'] = DatastreamCode
        config[id]['Name'] = Name
        config[id]['DatastreamCurrency'] = DatastreamCurrency

        ##Write
        with open(self.user_config, 'w') as f:
            config.write(f)


    def readCountryMeta(self, country):
        config = configparser.ConfigParser()
        config.read(self.user_config)
        d = []
        d.append(
            {
                'id': config[country]['id'],
                'DatastreamCode': config[country]['DatastreamCode'],
                'Name': config[country]['Name'],
                'DatastreamCurrency': config[country]['DatastreamCurrency']
            }
        )
        return pd.DataFrame(d).set_index('id')

    def readMetadata(self):
        config = configparser.ConfigParser()
        config.read(self.user_config)
        d = []
        for country in config.sections():
            d.append(
                {
                    'id': config[country]['id'],
                    'DatastreamCode': config[country]['DatastreamCode'],
                    'Name': config[country]['Name'],
                    'DatastreamCurrency': config[country]['DatastreamCurrency']
                }
            )
        return pd.DataFrame(d).set_index('id')



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
CountryMetaDataFile().addCountry("FRA", "FR", "France", "FRF")
CountryMetaDataFile().addCountry("CHE", "SW", "Switzerland", "CHF")

print(CountryMetaDataFile().readMetadata())



