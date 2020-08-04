
import pandas as pd
import os

from os.path import join, relpath, split, exists
from glob import glob


class DataLib:

    def __init__(self, data_dir, write_prefix='data'):
        self.data_dir = data_dir
        self.write_prefix = write_prefix

    def _prep_write(self, address, data, suffix='.parquet'):
        outdir = join(self.data_dir, address)
        os.makedirs(outdir, exist_ok=True)
        data_file = join(outdir, self.write_prefix + suffix)
        if hasattr(data.index.dtype, "freq"):
            data = data.to_timestamp()
        return data, data_file

    def write_csv(self, address, data):
        data, data_file = self._prep_write(address, data, suffix='.csv')
        data.to_csv(data_file, compression="gzip")

    def write_data(self, address, data):
        data, data_file = self._prep_write(address, data)
        data.to_parquet(data_file, compression="gzip")

    def list(self, prefix=""):
        for path in glob(join(self.data_dir, "**", self.write_prefix + "*"), recursive=True):
            print(relpath(split(path)[0], self.data_dir))

    def __call__(self, address, **kwargs):
        for ext, reader in [("parquet", pd.read_parquet)]:
            candidate_path = join(self.data_dir, address, self.write_prefix + "." + ext)
            if os.path.exists(candidate_path):
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
