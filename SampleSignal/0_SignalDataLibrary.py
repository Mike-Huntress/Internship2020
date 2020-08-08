from BasicSetupUtilities.MetaDataBuilder import CountryMetaDataFile
from DataIOUtilities.DataLib import DataLib, DatastreamPulls

countryList = ['USA', 'AUS', 'JPN', 'CAN', 'CHE', 'GBR', 'ESP', 'FRA', 'ITA', 'DEU']
countries = CountryMetaDataFile().readMetadata().loc[countryList]
start_date = '1980-01'



##Bespoke code name dictionaries
MSCIEquityDictionary = {
                        'US':'MSUSAML',
                        'AU':'MSAUSTL',
                        'JP':'MSJPANL',
                        'CN':'MSCNDAL',
                        'SW':'MSSWITL',
                        'UK':'MSUTDKL',
                        'ES':'MSSPANL',
                        'FR':'MSFRNCL',
                        'IT':'MSITALL',
                        'BD':'MSGERML'
}


dsPuller = DatastreamPulls(countries)
bondReturnIdx_locFX = dsPuller.ds_country_pull(lambda x: f'BM{x}10Y', start_date, 'RI', 'D')
longRates = dsPuller.ds_country_pull(lambda x: f'TR{x}10T', start_date, 'RY', 'M')
shortRates = dsPuller.ds_country_pull(lambda x: f'TR{x}2YT', start_date, 'RY', 'M')
riskfreeRates = dsPuller.ds_country_pull(lambda x: f'TR{x}Z3M', start_date, '', 'M')
equityPrices = dsPuller.ds_country_pull(lambda x: MSCIEquityDictionary[x], start_date, 'MSPI', 'D')
M2_usd = dsPuller.ds_country_pull(lambda x: f'{x}CMS2..B', start_date, '', 'M',list(filter(lambda x: x !='AUS', countryList)))
M1_usd = dsPuller.ds_country_pull(lambda x: f'{x}CMS1..B', start_date, '', 'M')
M3_usd = dsPuller.ds_country_pull(lambda x: f'{x}CMS3..B', start_date, '', 'M',list(filter(lambda x: x !='USA', countryList)))
currentAccountNominal_usd = dsPuller.ds_country_pull(lambda x: f'{x}CCUR..B', start_date, '', 'M')
currentAccount_pctGDP = dsPuller.ds_country_pull(lambda x: f'{x}CCUR..Q', start_date, '', 'M')
gdpNominal_usd = dsPuller.ds_country_pull(lambda x: f'{x}CGDP..A', start_date, '', 'M')
gdpReal = dsPuller.ds_country_pull(lambda x: f'{x}CGDP..D', start_date, '', 'M')
fxNomPrices_TrdWts = dsPuller.ds_country_pull(lambda x: f'{x}CXTW..F', start_date, '', 'M',['USA', 'AUS', 'JPN', 'CHE', 'GBR'])
fxRealPrices_TrdWts = dsPuller.ds_country_pull(lambda x: f'{x}CXTR..F', start_date, '', 'M',['USA', 'AUS', 'JPN', 'CHE', 'GBR'])
fxVsUSD = dsPuller.ds_country_pull(lambda x: f'{x}XRUSD.', start_date, '', 'M')
coreCPI_SA = dsPuller.ds_country_pull(lambda x: f'{x}CCOR..E', start_date, '', 'M')


##Write to library
dl = DataLib("SignalData")
dl.write_data("BondRetIdx/LocalFX",bondReturnIdx_locFX.to_timestamp())
dl.write_data("LongRates",longRates.to_timestamp())
dl.write_data("ShortRates", shortRates.to_timestamp())
dl.write_data("RiskfreeRates", riskfreeRates.to_timestamp())
dl.write_data("EquityPrices", equityPrices.to_timestamp())
dl.write_data("M2/inUSD", M2_usd.to_timestamp())
dl.write_data("M1/inUSD", M1_usd.to_timestamp())
dl.write_data("M3/inUSD", M3_usd.to_timestamp())
dl.write_data("CurrAcctNom/inUSD", currentAccountNominal_usd.to_timestamp())
dl.write_data("CurrAcctPctGDP", currentAccount_pctGDP.to_timestamp())
dl.write_data("GDP/Nominal", gdpNominal_usd.to_timestamp())
dl.write_data("GDP/Real", gdpReal.to_timestamp())
dl.write_data("fxTrdWts/Nominal", fxNomPrices_TrdWts.to_timestamp())
dl.write_data("fxTrdWts/Real", fxRealPrices_TrdWts.to_timestamp())
dl.write_data("fxVsUSD", fxVsUSD.to_timestamp())
dl.write_data("CoreCPI/SA", coreCPI_SA.to_timestamp())

print("Success: Built Data Library")


