
from os.path import dirname, join

START_DATE = '1980-01'
COUNTRY_LIST = ['USA', 'AUS', 'JPN', 'CAN', 'CHE', 'GBR', 'ESP', 'FRA', 'ITA', 'DEU']
FX_COUNTRIES = ['USA', 'AUS', 'JPN', 'CHE', 'GBR']
COUNTRY_METADATA_FILEPATH = join(dirname(__file__), 'country_metadata.csv')
MSCI_EQUITY_CODES = {
    'US': 'MSUSAML',
    'AU': 'MSAUSTL',
    'JP': 'MSJPANL',
    'CN': 'MSCNDAL',
    'SW': 'MSSWITL',
    'UK': 'MSUTDKL',
    'ES': 'MSSPANL',
    'FR': 'MSFRNCL',
    'IT': 'MSITALL',
    'BD': 'MSGERML',
}
DATA_LIB_NAME = 'SignalData'
LOGGER_NAME = 'dataio'
