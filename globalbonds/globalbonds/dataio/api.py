
from pydatastream import Datastream
from logging import getLogger

from .data_stream import DatastreamPuller
from .data_lib import DataLib
from .constants import (
    START_DATE,
    COUNTRY_LIST,
    MSCI_EQUITY_CODES,
    FX_COUNTRIES,
    DATA_LIB_NAME,
    LOGGER_NAME,
)

logger = getLogger(LOGGER_NAME)


def pull_and_write_streams(user, password, data_dir=DATA_LIB_NAME):
    """Return a DataLib with all streams. Default settings only."""
    datastream = Datastream(username=user, password=password)
    logger.info('created datastream')
    logger.info('pulling streams...')
    dl = DataLib(data_dir)
    streams = pull_data_streams(datastream, existing_streams=set(dl.list()))
    logger.info('done pulling streams.')
    logger.info('writing streams...')
    data_lib = write_data_streams(data_dir, streams)
    logger.info('done writing streams.')
    return data_lib


def pull_data_streams(datastream, start_date=START_DATE, existing_streams=set()):
    """Return a dict mapping stream names to data streams."""
    puller = DatastreamPuller(datastream, start_date)
    streams = {
        "BondRetIdx-LocalFX": lambda: puller.pull(lambda x: f'BM{x}10Y', 'RI', 'D'),
        "LongRates": lambda: puller.pull(lambda x: f'TR{x}10T', 'RY'),
        "ShortRates": lambda: puller.pull(lambda x: f'TR{x}2YT', 'RY'),
        "EquityPrices": lambda: puller.pull(lambda x: MSCI_EQUITY_CODES[x], 'MSPI', 'D', country_ids=COUNTRY_LIST),
        "M1-inUSD": lambda: puller.pull(lambda x: f'{x}CMS1..B', country_blacklist=['NOR']),
        "M2-inUSD": lambda: puller.pull(lambda x: f'{x}CMS2..B', country_blacklist=['AUS']),
        "M3-inUSD": lambda: puller.pull(lambda x: f'{x}CMS3..B', country_blacklist=['USA']),
        "CurrAcctNom-inUSD": lambda: puller.pull(lambda x: f'{x}CCUR..B'),
        "CurrAcctPctGDP": lambda: puller.pull(lambda x: f'{x}CCUR..Q'),
        "GDP-Nominal": lambda: puller.pull(lambda x: f'{x}CGDP..A'),
        "GDP-Real": lambda: puller.pull(lambda x: f'{x}CGDP..D'),
        "fxTrdWts-Nominal": lambda: puller.pull(lambda x: f'{x}CXTW..F', country_ids=FX_COUNTRIES),
        "fxTrdWts-Real": lambda: puller.pull(lambda x: f'{x}CXTR..F', country_ids=FX_COUNTRIES),
        "fxVsUSD": lambda: puller.pull(lambda x: f'{x}XRUSD.'),
        "CoreCPI-SA": lambda: puller.pull(lambda x: f'{x}CCOR..E'),
        "RiskFree-Rate": lambda: puller.pull(lambda x: f'{x}GBILL3', country_ids=['USA', 'GBR']),
    }
    out = {}
    for key, pull_stream in streams.items():
        if key in existing_streams:
            continue
        out[key] = pull_stream()
    return out


def write_data_streams(data_dir, streams):
    """Return a DataLib that all streams have been written to."""
    dl = DataLib(data_dir)
    for stream_name, stream in streams.items():
        dl.write_data(stream_name, stream.to_timestamp())
    return dl
