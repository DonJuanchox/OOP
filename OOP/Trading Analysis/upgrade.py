import etl_tools as etl
from etl_logger import get_logger
import pathlib
import csv
import pandas as pd
import tools
import logging

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
fx_rate_df.set_index('ccy_pair', inplace=True)
fx_rate = fx_rate_df['rate'].to_dict()

# Create unique ids per trade
trading_df['main_id'] = trading_df\
    .apply(tools.generate_id, axis=1)
clearing_df['main_id'] = clearing_df\
    .apply(tools.generate_id, axis=1)

# Function to find a rate based on the substring (currency) in fx_rate
def get_rate(logger, dictionary, sub_string):
    for key in dictionary.keys():
        if sub_string in key:
            return dictionary[key]  # Return the rate from the dictionary
    logger.warning('No key contains the specified substring.')
    return None  # Return None if no matching key is found
# Convert values to EUR
trading_df['fx_eur_rate'] = trading_df\
    .apply(lambda row: get_rate(logger, fx_rate, row['currency']), axis=1)
clearing_df['fx_eur_rate'] = clearing_df\
    .apply(lambda row: get_rate(logger, fx_rate, row['currency']), axis=1)


trading_df['eur_price'] = trading_df['fx_eur_rate'] * trading_df['price']
trading_df['eur_net_position_trading'] = trading_df['fx_eur_rate'] * trading_df['net_position_trading']

clearing_df['eur_price'] = clearing_df['fx_eur_rate'] * clearing_df['price']
clearing_df['eur_net_position_clearing'] = clearing_df['fx_eur_rate'] * clearing_df['net_position_clearing']

# -- groupby data first
trading_df = trading_df.fillna(0).groupby(by=['symbol', 'product_type', 'put_call',
                      'strike', 'maturity_date', 'eur_price', 'main_id'], as_index=False)\
      .agg({'eur_net_position_trading': 'sum'})

clearing_df = clearing_df.fillna(0).groupby(by=['symbol', 'product_type', 'put_call',
                      'strike', 'maturity_date', 'eur_price', 'main_id'], as_index=False)\
      .agg({'eur_net_position_clearing': 'sum'})


# Merge tables
df_1 = trading_df.merge(clearing_df[['main_id', 'eur_net_position_clearing']],
                        how='left', on='main_id')

df_2 = clearing_df.merge(trading_df[['main_id', 'eur_net_position_trading']],
                          how='left', on='main_id')



df_1['break_in_eur'] = df_1[['eur_net_position_trading', 'eur_net_position_clearing']].apply(lambda row:
                                                      tools.get_position_break(row, 'eur_net_position_trading', 'eur_net_position_clearing'),
                                                      axis=1)

df_2['break_in_eur'] = df_2[['eur_net_position_clearing', 'eur_net_position_trading']].apply(lambda row:
                                                      tools.get_position_break(row, 'eur_net_position_clearing', 'eur_net_position_trading'),
                                                      axis=1)


df = pd.concat([df_1, df_2], ignore_index=True)\
    .loc[lambda x: x['break_in_eur'] != 0].reset_index(drop=True)\
    .fillna(0)

df.drop_duplicates(subset=['main_id'], inplace=True)
# df = df\
#     .groupby(by=['symbol', 'product_type', 'put_call',
#                  'strike', 'maturity_date', 'main_id'], as_index=False)\
#     .agg({'break_in_eur': 'sum'})

# Divide rows which have duplicated id
# df_not_duplicated = df[~df['main_id'].duplicated(keep=False)]\
#     .reset_index(drop=True)# not duplicated
# df_duplicated = df[df['main_id'].duplicated(keep='first')]\
#     .sort_values(['main_id'])\
#     .reset_index(drop=True)
# df = pd.concat([df_not_duplicated, df_duplicated])
df.to_csv('out.csv', index=False)


# print(df.groupby(by=['symbol', 'product_type', 'put_call',
#                       'strike', 'maturity_date'], as_index=False)\
#       .agg({'break_in_eur': 'sum'}))