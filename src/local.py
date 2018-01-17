# Saves the mined data into csv, pickle, sqlite

import os
import pickle

import pandas as pd

from src.web_scraper import get_omx_data, get_price_df
from src.utils import convert_date, convert_volume_format


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


def df_to_pickle(market, startdate, enddate, *args, target_path=False):
    """
    Saves the panda dataframe acquired from Googles Finance history search
    into a pickle dump for local usage so we don't have to do heavy processing
    power required work everytime.

    :param market: markets location, helsinki, iceland, stockholm etc.
    :param target_path: saving location, default: './.local/df_stock_pickle/'
    :param startdate: list history from startdate
    :param enddate: list history to enddate
    """
    # path for symbols
    symbol_path = './.local/symbols_list/'
    if not target_path:
        # path for saving the locations
        target_path = './.local/df_stock_pickle/'

        if not os.path.exists('./.local/df_stock_pickle/'):
            os.mkdir('./.local/df_stock_pickle/')

    MARKET = {'helsinki':'HEL'}
    # naming convention for pickle dump
    symbols = 'OMX_{:s}_symbols.pickle'.format(market)

    with open((symbol_path + symbols),'rb') as symbol_file:
        symbols_list = pickle.load(symbol_file)

    for symbol in symbols_list: 

        if not os.path.exists(target_path+symbol+'.pickle'):
            df = get_price_df(symbol, startdate, enddate, market=MARKET[location])

            with open(target_path+symbol+'.pickle','wb') as f:
                pickle.dump(df,f)
        else:
            print('Already have it')


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


def pickle_to_csv(pickles_path, new_path):
    """
    Converts the aquired pickle dumps to .csv files

    :param pickles_path: path for pickle dumps
    :param new_path: path to new csv
    """
    # make the directory for the csv files
    if not os.path.exists(new_path):
        os.mkdir(new_path)

    # keeping track of handled files
    handled = []
    for file_name in os.listdir(pickles_path):

        if file_name not in handled:
            with open(pickles_path + file_name, 'rb') as f:

                df = pickle.load(f)

                # converts dates into unified format and sets them as index
                df['date'] = df['date'].apply(convert_date)
                df['volume'] = df['volume'].apply(convert_volume_format)
                df.set_index('date',inplace=True)

                csv = df.to_csv(new_path + "{:}.csv".format(file_name.strip('.pickle')))

                handled.append(file_name)
