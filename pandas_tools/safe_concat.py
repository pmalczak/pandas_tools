# -*- coding: utf-8 -*-
__author__ = 'Piotr.Malczak@gpm-sys.com'

from typing import Union

import pandas as pd


def safe_concat(df1: pd.DataFrame, df2: pd.DataFrame) -> pd.DataFrame:
    s1, s2 = set(df1.columns), set(df2.columns)

    sd = s1.symmetric_difference(s2)
    if len(sd) == 0:
        return pd.concat([df1, df2])

    if len(df1) == 0:
        return df2
    if len(df2) == 0:
        return df1

    if len(s1) > len(s2):
        cols = list(s1 - s2)
        df2 = _unite_by_extension(df2, df1, cols)
        return pd.concat([df1, df2])

    elif len(s1) < len(s2):
        return safe_concat(df2, df1)

    else:  # len s1 == len s2  - the same lenght, other content
        cols = list(s1 - s2)
        df2 = _unite_by_extension(df2, df1, cols)

        s1, s2 = set(df1.columns), set(df2.columns)
        cols = list(s2 - s1)
        df1 = _unite_by_extension(df1, df2, cols)
        return pd.concat([df1, df2])


def _unite_by_extension(target: pd.DataFrame, source: pd.DataFrame, cols: list) -> pd.DataFrame:
    if len(target) > 0:
        assert len(target.columns) <= len(source.columns)
        for column in cols:
            _dtype = source.dtypes[column]
            target[column] = _dtype_initial_value(_dtype)
            target[column] = target[column].astype(_dtype)
    return target


def _dtype_initial_value(_dtype) -> Union[int, float, str]:
    _map = {
        'int64': 0,
        'int32': 0,
        'float64': 0.0,
        'object': '',
        'string': '',
    }
    try:
        result = _map[_dtype.name]
    except KeyError:
        raise
    return result
