import pandas as pd
from functools import lru_cache
from pandas.util import hash_pandas_object
from hashlib import sha256
import math
import numpy as np


def _index_marks(nrows, chunk_size):
    return range(chunk_size, math.ceil(nrows / chunk_size) * chunk_size, chunk_size)


def split_df(dfm, chunk_size):
    indices = _index_marks(dfm.shape[0], chunk_size)
    chunks = np.split(dfm, indices)
    return chunks


class HashableDataFrame(pd.DataFrame):
    def __init__(self, obj):
        super().__init__(obj)

    def __hash__(self):
        hash_value = sha256(hash_pandas_object(self, index=True).values)
        hash_value = hash(hash_value.hexdigest())
        return hash_value

    def __eq__(self, other):
        return self.equals(other)


class HashableSeries(pd.Series):
    def __init__(self, obj):
        super().__init__(obj)

    def __hash__(self):
        hash_value = sha256(hash_pandas_object(self, index=True).values)
        hash_value = hash(hash_value.hexdigest())
        return hash_value

    def __eq__(self, other):
        return self.equals(other)


def make_hashable_pandas_object(obj):
    if type(obj) is pd.DataFrame:
        return HashableDataFrame(obj)
    elif type(obj) is pd.Series:
        return HashableSeries(obj)
    else:
        raise Exception(f'obj must be of type DataFrame or Series, '
                        f'but is {type(obj)}')
