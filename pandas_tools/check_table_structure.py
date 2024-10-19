# -*- coding: utf-8 -*-
__author__ = 'Piotr.Malczak@gpm-sys.com'
from typing import Iterable
from _collections_abc import dict_keys

import pandas

from validate_column import validate_column


def check_table_structure(actual_dataframe, expected_structure):
    if isinstance(expected_structure, dict):
        _check_table_columns(actual_dataframe.columns, expected_structure.keys())
        _check_columns_type(actual_dataframe, expected_structure)
    elif isinstance(expected_structure, (list, tuple, dict_keys)):
        _check_table_columns(actual_dataframe.columns, expected_structure)
    else:
        raise AttributeError
    return


def _check_table_columns(actual_columns: Iterable, expected_columns: Iterable):
    actual_columns = set(actual_columns)
    expected_columns = set(expected_columns)

    redundant = actual_columns - expected_columns
    missing = expected_columns - actual_columns
    m_redundant, m_missing = '', ''

    if redundant:
        m_redundant = f'\nredundant columns: {redundant}'
    if missing:
        m_missing = f'\n  missing columns: {missing}'

    if m_redundant or m_missing:
        m = f'{m_redundant}{m_missing}'
        raise AttributeError(m)


def _check_columns_type(actual_dataframe, expected_structure: dict):
    assert isinstance(expected_structure, dict)
    for column_name, column_description in expected_structure.items():
        if column_description is None:
            pass
        elif isinstance(column_description, list):
            validate_column(actual_dataframe, column_name, column_description)
        else:
            _check_column_assign_type(actual_dataframe, column_name, column_description)


def _check_column_assign_type(actual_dataframe, column_name, column_description):
    df_column_dtype_name = actual_dataframe.dtypes[column_name].name

    if isinstance(column_description, str):
        expected_type_name = column_description
    # elif isinstance(column_description, ):
    else:
        raise ValueError

    if expected_type_name == 'str' and df_column_dtype_name == 'object':
        pass
    else:
        if not df_column_dtype_name.startswith(expected_type_name):
            # if expected_type_name != df_column_dtype_name:
            m = f'expected column type of "{column_name}" = "{expected_type_name}", got "{df_column_dtype_name}" instead'
            raise AttributeError(m)
