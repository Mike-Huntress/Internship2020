import sys
sys.path.append('.')

from BasicSetupUtilities.MetaDataBuilder import CountryMetaDataFile

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