# -*- coding: utf-8 -*-
__author__ = 'Piotr.Malczak@gpm-sys.com'
import pandas as pd
from safe_concat import safe_concat


class DfSplitterCore:
    def __init__(self, df: pd.DataFrame, split_cond: (dict, pd.Series), close_on_exit=True):
        if not isinstance(df, pd.DataFrame):
            raise AttributeError('Pandas DataFrame required')
        self.split_cond = split_cond
        self.df = df
        self.result: pd.DataFrame = None
        self.negative = None
        self.positive = None
        self.close_on_exit = close_on_exit

    def __str__(self):
        try:
            p, n = len(self.positive), len(self.negative)
            return f'pos:{p} neg:{n}'
        except Exception:
            return f'{len(self.result)}'

    def remove_positive(self):
        if len(self.positive) > 0:
            self.positive = self.positive[0:0]

    def remove_negative(self):
        if len(self.negative) > 0:
            self.negative = self.negative[0:0]

    def remove_all(self):
        self.remove_positive()
        self.remove_negative()

    def __enter__(self):
        if isinstance(self.split_cond, dict):
            assert len(self.split_cond) == 1
            for column, value in self.split_cond.items():
                if isinstance(value, (str, int)):
                    cond = self.df[column] == value
                elif isinstance(value, (list, tuple)):
                    cond = self.df[column].isin(value)
                elif callable(value):
                    cond = value(self.df[column])
                else:
                    raise AttributeError
                self.positive = self.df[cond]
                self.negative = self.df[~cond]
        elif isinstance(self.split_cond, pd.Series):
            self.positive = self.df[self.split_cond]
            self.negative = self.df[~self.split_cond]
        else:
            raise AttributeError(self.split_cond)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if all((exc_type, exc_val, exc_tb)):
            raise

        if len(self.positive) == 0 and len(self.negative) > 0:
            self.result = self.negative

        elif len(self.negative) == 0 and len(self.positive) > 0:
            self.result = self.positive

        else:
            self.result = safe_concat(self.positive, self.negative)

        if self.close_on_exit:
            delattr(self, 'positive')
            delattr(self, 'negative')
        return


class DfSplitter(DfSplitterCore):

    def __enter__(self):
        if isinstance(self.split_cond, dict):
            cond_dict(self, self.split_cond)
        elif isinstance(self.split_cond, pd.Series):
            self.positive = self.df[self.split_cond]
            self.negative = self.df[~self.split_cond]
        else:
            raise AttributeError
        return self


def cond_dict(self: DfSplitter, cond: dict):
    assert self.positive is None
    assert self.negative is None

    positive = self.df
    for column, value in cond.items():
        positive, negative = _select_(positive, column, value)
        self.positive = positive
        self.negative = pd.concat([self.negative, negative])
    assert len(self.df) == len(self.positive) + len(self.negative)
    return


def _select_(df, column, value):
    if isinstance(value, (str, int, float)):
        cond = df[column] == value
    elif isinstance(value, (list, tuple)):
        cond = df[column].isin(value)
    elif isinstance(value, set):
        _value_set = list(value)
        cond = df[column].isin(_value_set)
    elif callable(value):
        cond = value(df[column])
    else:
        raise AttributeError

    positive = df[cond]
    negative = df[~cond]
    return positive, negative
