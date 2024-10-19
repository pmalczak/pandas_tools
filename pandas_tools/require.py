# -*- coding: utf-8 -*-
__author__ = 'Piotr.Malczak@gpm-sys.com'

import pandas as pd


class MissingColumnsInDataFrame(Exception):
    pass


class MissingValuesInDataFrameColumn(Exception):
    pass


def require(data, required_columns=None) -> None:
    assert isinstance(data, pd.DataFrame)
    assert isinstance(required_columns, (tuple, list))

    data_columns = data.columns.tolist()
    if isinstance(data_columns[0], tuple):
        data_columns = list(map(lambda x: ''.join(x), data_columns))
    result = set(required_columns) - set(data_columns)
    if len(result) > 0:
        raise MissingColumnsInDataFrame(result)


def require_value(series, required_values=None) -> None:
    assert isinstance(series, pd.Series)
    assert isinstance(required_values, (list, tuple, set))
    _series = set(series.tolist())
    r = set()
    for item in required_values:
        if item not in _series:
            r.add(item)
    if r:
        raise MissingValuesInDataFrameColumn(r)
