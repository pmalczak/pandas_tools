# -*- coding: utf-8 -*-
__author__ = 'Piotr.Malczak@gpm-sys.com'
import math


def validate_column(data_frame, column_name: str, the_enum: list):
    def _none_mapping(x):
        if x is None:
            return 'None'
        elif isinstance(x, (str)):
            return x
        elif math.isnan(x):
            return 'None'
        raise ValueError
        # return x

    df_col_values = data_frame[column_name].unique().tolist()
    df_col_values = set(map(_none_mapping, df_col_values))

    expected_values = set(map(_none_mapping, the_enum))
    diff = df_col_values - expected_values
    if diff:  # print warning
        m = f'unexpected value/s "{diff}" in column "{column_name}"'
        raise ValueError(m)
    return
