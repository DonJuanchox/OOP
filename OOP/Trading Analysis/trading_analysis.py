"""
TODO:
    - Create read/load csv file func -->  improve etl_tools func
    - adjust better how the col names are defined, seems a bit difficult to follow
    - add log to mention currency is not in the file - Create test case
    - Complicate a bit more the case in which two keys contain 'BRL'
    - Create ID to map values in the future:
        - symbol	product_type	put_call	strike	net_position_clearing	net_position_trading	position break
    - Calculate the following -> Value of option=net_position×multiplier×price
"""

import etl_tools as etl
from etl_logger import get_logger
import pathlib
import csv
import pandas as pd
import tools
import logging

logger = get_logger('Logg', logging.WARNING, [logging.StreamHandler()])

# Extract
file_folder = pathlib.Path(r'C:\Users\juann\OneDrive\Documentos\GitHub\OOP\Trading Analysis')
trading_file = file_folder.joinpath('trading_data.csv')
clearing_file = file_folder.joinpath('clearing_data.csv')
fx_file = file_folder.joinpath('fx_rate.csv')

# Load
trading_df: pd.DataFrame = etl.load_csv(trading_file, parse_dates=True)\
    .rename(columns={'net_position': 'net_position_trading'})
clearing_df: pd.DataFrame = etl.load_csv(clearing_file, parse_dates=True)
fx_rate_df: pd.DataFrame = etl.load_csv(fx_file)

# Data Wrangle
fx_rate_df.set_index('ccy_pair', inplace=True)
fx_rate = fx_rate_df['rate'].to_dict()

# Create unique ids per trade
trading_df['main_id'] = trading_df\
    .apply(tools.generate_id, axis=1)
clearing_df['main_id'] = clearing_df\
    .apply(tools.generate_id, axis=1)

# Convert values to EUR
trading_df['price_eur'] = trading_df\
    .apply(lambda row:tools.calculate_rate(logger, row, fx_rate), axis=1)
clearing_df['price_eur'] = clearing_df\
    .apply(lambda row: tools.calculate_rate(logger, row, fx_rate), axis=1)

# Calculate position break
trading_df['position_break_amount'] = trading_df[['net_position', 'net_position_clearing']]\
    .apply(lambda row:
           tools.get_position_break(row, 'net_position', 'net_position_clearing'),
           axis=1)
clearing_df['position_break_amount'] = clearing_df[['net_position', 'net_position_trading']]\
    .apply(lambda row:
           tools.get_position_break(row, 'net_position', 'net_position_trading'),
           axis=1)
# Filter to positions in which there is a position break




