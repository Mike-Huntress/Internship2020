
import pandas as pd

from .constants import COUNTRY_METADATA_FILEPATH


def country_metadata(path=COUNTRY_METADATA_FILEPATH):
    """Return a DataFrame with country metadata."""
    tbl = pd.read_csv(path, index_col=0)
    return tbl
