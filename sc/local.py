import os
import pickle

import pandas as pd

from web_scraper import get_omx
from scrap_google import data_frame
from utils import convert_date, conver_volume_format


# Saves the mined data into a .pickle dumps, compiles and converts them
# for further use.


def get_symbols(location):
    """
    Gets symbol list and saves it to pickle dump

    :param location: market location, helsinki, iceland, stockholm etc.
    :param dpath: directory path that pickle dump is saved into.
    """
    # target name for saved file.
    target = 'OMX_{:s}_symbols.pickle'.format(location)
    # directory path that list of symbols is saved into.
    symbols_dir = './.local/symbols_list/'

    if not os.path.exists(symbols_dir):
        os.mkdir(symbols_dir)

    if not os.path.exists(symbols_dir + target):
        with open((symbols_dir + target), 'wb') as f:
            data = get_omx(location)
            pickle.dump(data, f)


def get_df(location, startdate, enddate, target_path=False):
    """
    Saves the panda dataframe acquired from Googles Finance history search
    into a pickle dump for local usage so we don't have to do heavy processing
    power required work everytime.

    :param location: markets location, helsinki, iceland, stockholm etc.
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
    
    # TODO: Add all of the markets
    m = {'helsinki':'HEL'}
    # naming convention for pickle dump
    symbols = 'OMX_{:s}_symbols.pickle'.format(location)
    
    with open((symbol_path + symbols),'rb') as symbol_file:
        symbols_list = pickle.load(symbol_file)
    
    for symbol in symbols_list: 

        if not os.path.exists(target_path+symbol+'.pickle'):
            df = data_frame(symbol, startdate, enddate, market=m[location])

            with open(target_path+symbol+'.pickle','wb') as f:
                pickle.dump(df,f)
        else:
            print('Already have it')


def compile_data(market, column, target_path=False):
    """
    Compiles data from all of the pickle dumps to one .csv file.

    :param market: to specify saved file
    :param column: type we're joining [date,open,high,low,close,volume]
    :param target_path: path to save compiled data into, default: './.local/df_compiled/'
    """
    # path for symbols
    symbols_path = './.local/symbols_list/'
    # path for stock data frames
    df_path = './.local/df_stock_pickle/'

    symbols_file = symbols_path + 'OMX_{:s}_symbols.pickle'.format(market)

    with open(symbols_file,'rb') as f:
        symbols_list = pickle.load(f)

    if not os.path.exists('./.local/df_compiled'):
        os.mkdir('./.local/df_compiled')

    new_df = pd.DataFrame()

    for symbol in symbols_list:
        with open(df_path + symbol + '.pickle', 'rb') as f:
            df = pickle.load(f)
        
        df['date'] = df['date'].apply(convert_date)
        df.set_index('date',inplace=True)
        
        df.drop(['open','high','low','volume'], 1, inplace=True)
        df.rename(columns = {column: symbol}, inplace=True)
        
        if new_df.empty:
            new_df = df
        else:
            new_df =  new_df.join(df,how='outer')
        
    # we can select to save the file into specific directory
    if not target_path:
        new_df.to_csv('./.local/df_compiled/OMX_{:s}_joined_{:s}.csv'.format(market,column))
    else:
        new_df.to_csv(target_path + 'OMX_{:s}_joined_{:s}.csv'.format(market,column))


def pickle_to_csv():
    """
    Converts the aquired pickle dumps to .csv files
    """

    # path for pickle dumps
    pickles_path = './.local/df_stock_pickle/'
    
    # make the directory for the csv files
    new_path = './.local/df_stock_csv/'
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
                df['volume'] = df['volume'].apply(conver_volume_format)
                df.set_index('date',inplace=True)
                
                csv = df.to_csv(new_path + "{:}.csv".format(file_name.strip('.pickle')))

                handled.append(file_name)
