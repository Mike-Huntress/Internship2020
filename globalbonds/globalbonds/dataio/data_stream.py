
import pandas as pd
from logging import getLogger

from .utils import country_metadata
from .constants import LOGGER_NAME

logger = getLogger(LOGGER_NAME)


class DatastreamPuller:

    def __init__(self, datastream, start_date, countries=country_metadata()):
        self.ds = datastream
        self.start_date = start_date
        self.countries = countries
        self.country_ids = list(self.countries.index)

    def pull(self, tick_format, ds_fields='', freq='M', country_ids=None, country_blacklist=[]):
        country_ids = self.country_ids if not country_ids else country_ids
        country_ids = [cid for cid in country_ids if cid not in country_blacklist]
        country_ids = self.countries.loc[country_ids]['datastream_code']
        tickers = [tick_format(c) for c in country_ids]
        logger.info(f'pulling tickers {tickers}')
        if isinstance(ds_fields, str):
            tickerDict = dict(zip(tickers, self.country_ids))
            data = self.ds.fetch(
                tickers, fields=ds_fields, freq=freq, date_from=self.start_date
            ).unstack(0).to_period(freq)
            dataCols = [cols[1] for cols in data.columns]
            data.columns = [tickerDict[tick] for tick in dataCols]
        elif callable(ds_fields):
            pulls = []
            for country, ticker in zip(self.country_ids, tickers):
                ds_field = ds_fields(country)
                data = self.ds.fetch(
                    ticker, fields=ds_field, freq=freq, date_from=self.start_date
                ).to_period(freq)
                data.columns = [country]
                pulls.append(data)
            data = pd.concat(pulls, axis=1)
        data = data.rename_axis("country", axis="columns").rename_axis("date", axis="rows")
        return data
