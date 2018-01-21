# Saves the mined data into csv, pickle, sqlite

import os
import pickle

import pandas as pd

from src.web_scraper import get_omx_data, get_price_google, get_omx_markets
from src.utils import convert_date

def initialize_symbols(path):
    """
    Get the symbols for markets.

    :param path: path to local data
    """
    if not os.path.exists(path):
        os.mkdir(path)

    markets_data = get_omx_markets()
    markets_to_pickle('OMX', markets_data, path)
    symbols = []
    for market in markets_data:
        symbols_data = get_omx_data(market, 0, 1, 4, 5)

        symbols.append(symbols_data)
        symbols_to_pickle(symbols_data, market, path)

    return markets_data, symbols
    

def symbols_to_pickle(symbols, market, path):
    """
    Gets symbol list and saves it to pickle dump

    :param market: market location, helsinki, iceland, stockholm etc.
    :param path: directory path that pickle dump is saved into.
    """
    # target name for saved file.
    target = 'OMX_{:s}_symbols.pickle'.format(market)
    # directory path that list of symbols is saved into.
    symbols_dir = '{:s}/symbols_pickles/'.format(path)

    if not os.path.exists(symbols_dir):
        os.mkdir(symbols_dir)

    target = symbols_dir + target
    if not os.path.exists(target):
        with open(target, 'wb') as f:
            pickle.dump(symbols, f)
    else:
        with open(target, 'rb') as f:
            symbols_old = pickle.load(f)

        if symbols != symbols_old:
            with open(target, 'wb') as f:
                pickle.dump(symbols, f)


def markets_to_pickle(market, data, path):
    """
    Saves list of markets into pickles dump

    :param markets:
    :param data:
    :param path:
    """
    directory = '{:s}/markets_list/'.format(path)

    target = directory + '{:s}_markets_list.pickle'.format(market)

    if not os.path.exists(directory):
        os.mkdir(directory)

    if not os.path.exists(target):
        with open(target, 'wb') as f:
            pickle.dump(data, f)


def compile_data(market, column, symbols_path, df_path, target_path=False):
    """
    Compiles data from all of the pickle dumps to one .csv file.

    :param market: to specify saved file
    :param column: type we're joining [date,open,high,low,close,volume]
    :param symbols_path: path for symbols
    :param df_path: path for stock data frames
    :param target_path: path to save compiled data into, default: './.local/df_compiled/'
    """
    symbols_file = symbols_path + 'OMX_{:s}_symbols.pickle'.format(market)

    with open(symbols_file,'rb') as f:
        symbols_list = pickle.load(f)

    new_df = pd.DataFrame()

    for symbol in symbols_list:
        with open(df_path + symbol + '.pickle', 'rb') as f:
            df = pickle.load(f)

        df['date'] = df['date'].apply(convert_date)
        df.set_index('date', inplace=True)

        #TODO replace the drop to handle the column param
        df.drop(['open','high','low','volume'], 1, inplace=True)
        df.rename(columns = {column: symbol}, inplace=True)

        if new_df.empty:
            new_df = df
        else:
            new_df =  new_df.join(df, how='outer')

    # we can select to save the file into specific directory
    if not target_path:
        return new_df
    else:
        if not os.path.exists('./.local/df_compiled'):
            os.mkdir('./.local/df_compiled')
        new_df.to_csv(target_path + 'OMX_{:s}_joined_{:s}.csv'.format(market,column))
