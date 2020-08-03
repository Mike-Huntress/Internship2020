import sys
sys.path.append('.')

import glob
import os
import pandas as pd
from BasicSetupUtilities.CredentialsStoreBuilder import DataSourceCredentials


class DataLib:
    def __init__(self, write_prefix):
        self.base_dir = os.path.expanduser(os.path.join("~", ".datalib"))
        self.data_filename = "data"
        self.write_prefix = write_prefix

    """
        @param address
        @param data
    """
    def write_csv(self, address, data):
        outdir = os.path.join(self.base_dir,self.write_prefix,address)
        if not os.path.exists(outdir):
            os.makedirs(outdir)

        data_file= os.path.join(outdir, self.data_filename + ".csv")
        data.to_csv(data_file)

        schema_file = os.path.join(outdir, 'schema.csv')
        schema = pd.concat([
            pd.Series([data.index.dtype], index=["index"]),
            data.dtypes
        ])
        schema.to_csv(schema_file)

    def write_data(self, address, data):
        outdir = os.path.join(self.base_dir,self.write_prefix,address)
        if not os.path.exists(outdir):
            os.makedirs(outdir)
        data_file = os.path.join(outdir, self.data_filename + ".parquet")
        if (hasattr(data.index.dtype, "freq")):
            data = data.to_timestamp()
        data.to_parquet(data_file, compression="gzip")#, times='int96'

    def lst(self, prefix = ""):
        for path in glob.glob(os.path.join(self.base_dir, prefix, "**", self.data_filename + "*"), recursive=True):
            print(os.path.relpath(os.path.split(path)[0], self.base_dir))

    def __call__(self, address, **kwargs):
        for (ext,reader) in zip(["parquet"], [pd.read_parquet]):
            candidate_path = os.path.join(self.base_dir, self.write_prefix, address, self.data_filename + "." + ext)
            if (os.path.exists(candidate_path)):
                return reader(candidate_path, **kwargs)

    def pull(self, address, name=None):
        df = self.__call__(address)
        if df is not None:
            if hasattr(df, "date"):
                df.date = df.date.apply(lambda x: pd.Period(x, freq='M'))
                df = df.set_index(df.date, drop=True)
            else:
                df = df.to_period()
            if name:
                df.columns = pd.MultiIndex.from_product([[name], df.columns])
            return df
        return None

    def pull_all(self, names, name2address):
        dfs = [self.pull(name2address(name), name) for name in names]
        return pd.concat(dfs, axis=1)

class DatastreamPulls:
    def __init__(self, country_info):
        # Dataframe keyed on standard countries, with DatastreamCode column
        self.country_info = country_info

    def getCountries(self):
        return self.country_info.index

    def ds_country_pull(self, tick_format, start_date, ds_fields, freq, countries = None, format_from_dscode=True):
        if countries is None:
            countries = self.getCountries()
        if format_from_dscode:
            pulled_countries = self.country_info.loc[countries]
            tickers = [tick_format(c) for c in pulled_countries.DatastreamCode]
        else:
            tickers = [tick_format(c) for c in countries]
        if isinstance(ds_fields, str):
            tickerDict = dict(zip(tickers,countries))
            data = datastream.fetch(tickers, fields=ds_fields, freq=freq, date_from=start_date)
            if(len(countries)<2):
                data = data.to_period(freq)
                data.columns = countries
            else:
                data = data.unstack(0).to_period(freq)
                dataCols = [cols[1] for cols in data.columns]
                data.columns = [tickerDict[tick] for tick in dataCols]
        elif callable(ds_fields):
            pulls = []
            for (country,ticker) in zip(countries,tickers):
                ds_field = ds_fields(country)
                data = datastream.fetch(ticker, fields=ds_field, freq=freq, date_from=start_date).to_period(freq)
                data.columns = [country]
                pulls.append(data)
            data = pd.concat(pulls, axis=1)
        else:
            raise "ds_fields must be string or function"
        return data.rename_axis("country",axis="columns").rename_axis("date",axis = "rows")


def getkey(name):
    return DataSourceCredentials().readCredentials(name)

# class Quandl:
#     def __init__(self, key):
#         self.key = key
#
#     def get(self, quandl_code, local_id, prov_container = None, **kwargs):
#         if prov_container is not None:
#             prov_container[local_id] = dict(
#                 src  = "quandl",
#                 code = quandl_code,
#                 date_acquired = datetime.utcnow(),
#                 quandl_params = kwargs
#             )
#         column = raw_quandl.get(quandl_code, api_key=self.key, **kwargs).rename(columns={"Value":local_id})
#         return column


# quandl = Quandl(getkey("quandl"))

def DatastreamInit():
    from pydatastream import Datastream
    key = getkey("datastream")
    return Datastream(username=key.user, password=key.password)
datastream = DatastreamInit()
