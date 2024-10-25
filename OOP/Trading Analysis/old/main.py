"""
This file aims toidentify any breaks between the ‘Trading Positions’
and the ‘Clearing Positions’ 
"""
import etl_tools as etl
from etl_logger import get_logger
import pathlib
import csv
import pandas as pd
import tools
import logging


"""
Set up logger.
Extract data from the folder.
Load data using pandas.
FX_file only contains two rows, it is possible to load the data without pandas
"""
# Set up logger
logger = get_logger('Logg', logging.WARNING, [logging.StreamHandler()])

# Extract
file_folder = pathlib.Path(
    r'C:\Users\juann\OneDrive\Documentos\GitHub\OOP\Trading Analysis')
trading_file = file_folder.joinpath('trading_data.csv')
clearing_file = file_folder.joinpath('clearing_data.csv')
fx_file = file_folder.joinpath('fx_rate.csv')

# Load
trading_df: pd.DataFrame = etl.load_csv(trading_file, parse_dates=True)\
    .rename(columns={'net_position': 'net_position_trading'})
clearing_df: pd.DataFrame = etl.load_csv(clearing_file, parse_dates=True)\
    .rename(columns={'net_position': 'net_position_clearing'})
fx_rate_df: pd.DataFrame = etl.load_csv(fx_file)

"""
Data Wrangle:
    - Convert Fx_rate dataframe into a dictionary
    - Create an unique id to identify each trade
    - Get the fx_rate value for a given currency
"""
# Dictionary -> {fx_pair:eur_rate}
fx_rate_df.set_index('ccy_pair', inplace=True)
fx_rate = fx_rate_df['rate'].to_dict()

# Id per trade
trading_df['main_id'] = trading_df\
    .apply(lambda row: tools.generate_id(row,['symbol','product_type','put_call', 'strike', 
                                          'maturity_date']), axis=1)
clearing_df['main_id'] = clearing_df\
    .apply(lambda row: tools.generate_id(row, ['symbol','product_type','put_call', 'strike', 
                                          'maturity_date']), axis=1)

# fx_rate conversion
trading_df['fx_eur_rate'] = trading_df\
    .apply(lambda row: tools.get_rate(logger, fx_rate, row['currency']), axis=1)
clearing_df['fx_eur_rate'] = clearing_df\
    .apply(lambda row: tools.get_rate(logger, fx_rate, row['currency']), axis=1)

"""
Group data as there might be rows with similar values:
    - e.g There might be a trade ABEVOPPut21.8212/17/2021 which is duplicate,
    however, they might have different net_positions.
"""
# Groupby data first
trading_df = trading_df.fillna(0).groupby(by=['symbol', 'product_type', 'put_call',
                      'strike', 'maturity_date', 'price', 'main_id', 'multiplier', 'fx_eur_rate'], as_index=False)\
      .agg({'net_position_trading': 'sum'})

clearing_df = clearing_df.fillna(0).groupby(by=['symbol', 'product_type', 'put_call',
                      'strike', 'maturity_date', 'price', 'main_id', 'multiplier', 'fx_eur_rate'], as_index=False)\
      .agg({'net_position_clearing': 'sum'})

# Calculate eur
trading_df['eur_net_position_trading'] = round((trading_df['fx_eur_rate'] * trading_df['net_position_trading']), 2)
clearing_df['eur_net_position_clearing'] = round((clearing_df['fx_eur_rate'] * clearing_df['net_position_clearing']), 2)

#Merge data
out_df = trading_df.merge(clearing_df[['main_id', 'eur_net_position_clearing']],
                        how='left', on='main_id')

# Get position break
out_df['break_in_eur'] = out_df['eur_net_position_clearing'].fillna(0) - out_df['eur_net_position_trading'].fillna(0)
out_df = out_df.loc[lambda x: x['break_in_eur'] != 0].reset_index(drop=True)

# Generate output
out_df.to_csv('break_position.csv', index=False)
